CREATE OR REPLACE VIEW potential_vendor_siblings AS (
WITH base AS (
SELECT
  vc.vendor_customer_id,
  vc.vendor_name,
  vc.normalized_vendor_customer_name,
  vc.first3_token,
  vc.billing_state,
  vc.normalized_billing_zip,
  p.parent_account_name,
  p.parent_account_id
FROM vendor_customers vc

LEFT JOIN vendor_customer_to_parent_account_map pid ON 
  vc.vendor_customer_id = pid.vendor_customer_id
LEFT JOIN parent_accounts p ON
  pid.parent_account_id = p.parent_account_id

WHERE 
  vc.first3_token IS NOT NULL
  AND vc.billing_state IS NOT NULL
  AND vc.normalized_billing_zip IS NOT NULL
), 

counted AS (
SELECT 
  *,
  COUNT(*) OVER (
  PARTITION BY first3_token, billing_state
  ) AS sibling_count
FROM base
), 

filtered AS (
SELECT 
  * 
FROM counted
WHERE sibling_count > 1
),

ranked AS (
SELECT 
  *,
  DENSE_RANK() OVER (
  ORDER BY first3_token, billing_state
  ) AS group_index

FROM filtered
)
SELECT 
  vendor_customer_id,
  vendor_name,
  normalized_vendor_customer_name,
  first3_token,
  billing_state,
  normalized_billing_zip,
  parent_account_name,
  parent_account_id,
  sibling_count,
  group_index
FROM ranked
ORDER BY group_index ASC
);

-- I want the parents assigned and I want the suggested parents
CREATE OR REPLACE VIEW suggested_vendor_parents AS (
SELECT DISTINCT
  base.group_index,
  base.first3_token,
  p.parent_account_id,
  p.parent_account_name,
  p.normalized_parent_name
FROM potential_vendor_siblings base
JOIN parent_accounts p ON 
  base.first3_token = p.first3_token
);