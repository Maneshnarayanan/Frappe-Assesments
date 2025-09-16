frappe.ready(function() {
  // Read ?shop=... from URL
  const params = new URLSearchParams(window.location.search);
  const shop = params.get("shop");

  if (shop) {
    // Set the "interested_shop" field in the form
    frappe.web_form.set_value("job_title", shop);
  }

  // After save redirect back to shop details page
  frappe.web_form.on('after_save', () => {
    if (shop) {
      window.location.href = `/shop?shop=${encodeURIComponent(shop)}&lead=success`;
    } else {
      window.location.href = `/shops?lead=success`;
    }
  });
});
