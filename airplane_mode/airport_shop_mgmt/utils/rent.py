
import frappe
from frappe.utils import get_first_day, get_last_day, add_days, nowdate
from datetime import date

def _settings():
    return frappe.get_single("Airport Shop Settings")

def _ym(dt):
    return f"{dt.year:04d}-{dt.month:02d}"

def ensure_monthly_rent(lease_name, target_month=None):
    lease = frappe.get_doc("Lease Contract", lease_name)
    if lease.status not in ("Active",):
        return

    # define period as the month that includes today unless target_month provided (YYYY-MM)
    today = date.today()
    if target_month:
        y, m = map(int, target_month.split("-"))
        period_start = date(y, m, 1)
    else:
        period_start = date(today.year, today.month, 1)

    period_end = get_last_day(period_start)
    billing_month = _ym(period_start)

    exists = frappe.db.exists(
        "Monthly Rent", {"contract": lease.name, "billing_month": billing_month}
    )
    if exists:
        return exists

    settings = _settings()
    amount = lease.rent_amount or settings.default_rent_amount or 0
    billing_day = lease.billing_day or 1
    due_days = settings.default_due_days or 7

    # billing date inside month (cap at last day)
    billing_date = date(period_start.year, period_start.month, min(billing_day, period_end.day))
    due_date = add_days(billing_date, due_days)

    doc = frappe.get_doc({
        "doctype": "Monthly Rent",
        "tenant": lease.tenant,
        "shop": lease.shop,
        "airport": lease.airport,
        "contract": lease.name,
        "billing_month": billing_month,
        "period_start": period_start,
        "period_end": period_end,
        "due_date": due_date,
        "amount": amount,
        "paid_amount": 0,
        "status": "Unpaid"
    })
    doc.insert(ignore_permissions=True)
    return doc.name

def generate_monthly_rents():
    """Run monthly (1st). Create rents for all active leases for the current month."""
    active_leases = frappe.get_all("Lease Contract",
        filters={"status": "Active"},
        pluck="name"
    )
    for l in active_leases:
        try:
            ensure_monthly_rent(l)
        except Exception:
            frappe.log_error(title="Monthly Rent Generation Failed", message=frappe.get_traceback())

def process_rent_reminders_daily():
    """Run daily. Only send emails on the configured reminder day, if enabled."""
    settings = _settings()
    if not settings.enable_rent_reminders:
        return

    from frappe.utils import now_datetime
    today = now_datetime().date()
    reminder_day = settings.reminder_day_of_month or 25
    if today.day != reminder_day:
        return

    # Upcoming dues for the current month or unpaid previous months
    unpaid = frappe.get_all("Monthly Rent",
        filters=[["status", "in", ["Unpaid", "Partially Paid"]]],
        fields=["name", "tenant", "shop", "airport", "amount", "due_date", "billing_month"]
    )

    template = settings.default_email_template or \
        "Dear {{ tenant }},\n\nThis is a friendly reminder that rent for {{ billing_month }} " \
        "amounting to {{ amount }} is due on {{ due_date }} for Shop {{ shop }} at {{ airport }}.\n\nThank you."

    for r in unpaid:
        try:
            tenant = frappe.get_doc("Tenant", r.tenant)
            if not tenant.email_id:
                continue
            ctx = {
                "tenant": tenant.tenant_name,
                "billing_month": r.billing_month,
                "amount": frappe.utils.fmt_money(r.amount),
                "due_date": frappe.utils.formatdate(r.due_date),
                "shop": r.shop,
                "airport": r.airport
            }
            msg = frappe.render_template(template, ctx)
            frappe.sendmail(
                recipients=[tenant.email_id],
                cc=[settings.cc_email] if settings.cc_email else None,
                subject=f"Rent Reminder: {r.billing_month} - {r.shop}",
                message=msg
            )
        except Exception:
            frappe.log_error(title="Rent Reminder Failed", message=frappe.get_traceback())

@frappe.whitelist()
def mark_overdue_rents_daily():
    """Mark rents as overdue if past due date + grace days."""
    settings = _settings()
    grace_days = settings.grace_days or 5

    today = date.today()
    rents = frappe.get_all("Monthly Rent",
        filters=[["status", "in", ["Unpaid", "Partially Paid"]]],
        fields=["name", "due_date"]
    )

    for r in rents:
        if r.due_date and today > add_days(r.due_date, grace_days):
            frappe.db.set_value("Monthly Rent", r.name, "status", "Overdue")
