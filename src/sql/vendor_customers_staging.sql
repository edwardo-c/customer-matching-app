WITH base AS (
SELECT DISTINCT ON (
    vendor_name, 
    raw_vendor_customer_name
  )
  vendor_name,
  raw_vendor_customer_name,
  normalized_vendor_customer_name,
  raw_billing_zip,
  normalized_billing_zip,
  billing_state,
  period_date,
  first3_token
FROM raw_vendor_customer_staging
ORDER BY vendor_name, raw_vendor_customer_name, period_date ASC, normalized_billing_zip, billing_state
), incoming AS (

SELECT 
  vendor_name,
  raw_vendor_customer_name,
  normalized_billing_zip
FROM base

EXCEPT 

SELECT 
  vendor_name,
  raw_vendor_customer_name,
  normalized_billing_zip
FROM vendor_customers

), expanded AS (
SELECT
  inc.vendor_name,
  inc.raw_vendor_customer_name,
  b.normalized_vendor_customer_name,
  b.raw_billing_zip,
  b.normalized_billing_zip,
  b.billing_state,
  b.period_date,
  b.first3_token
FROM incoming inc
JOIN base b ON 
  inc.vendor_name = b.vendor_name 
  AND inc.raw_vendor_customer_name = b.raw_vendor_customer_name
) SELECT * FROM expanded;
