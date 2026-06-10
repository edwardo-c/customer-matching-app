SELECT
  vendor_name,
  raw_vendor_customer_name,
  billing_zip,
  billing_state
FROM vendor_customer_staging

EXCEPT

SELECT
  vendor_name,
  raw_vendor_customer_name,
  billing_zip,
  billing_state
FROM vendor_customers