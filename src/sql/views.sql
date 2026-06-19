CREATE OR REPLACE VIEW suggested_vendor_siblings AS (
WITH parentless AS (
SELECT
  v.vendor_customer_id,
  v.vendor_name,
  v.raw_vendor_customer_name,
  v.normalized_vendor_customer_name,
  v.raw_billing_zip,
  v.normalized_billing_zip,
  v.billing_state,
  v.period_date,
  v.first3_token
FROM vendor_customers v
WHERE NOT EXISTS (
  SELECT 1 
  FROM vendor_customer_to_parent_account_map accepted
  WHERE v.vendor_customer_id = accepted.vendor_customer_id
  )
), 
potential_siblings_token_and_zip AS (
SELECT
  ps.vendor_customer_id AS left_vendor_customer_id,
  ps.vendor_name AS left_vendor_name,
  ps.raw_vendor_customer_name AS left_raw_vendor_customer_name,
  ps.normalized_vendor_customer_name AS left_normalized_vendor_customer_name,
  ps.normalized_billing_zip AS left_normalized_billing_zip,
  ps.billing_state AS left_billing_state,
  ps.first3_token AS left_first3_token,
  
  siblings.vendor_customer_id AS right_vendor_customer_id,
  siblings.vendor_name AS right_vendor_name,
  siblings.raw_vendor_customer_name AS right_raw_vendor_customer_name,
  siblings.normalized_vendor_customer_name AS right_normalized_vendor_customer_name,
  siblings.normalized_billing_zip AS right_normalized_billing_zip,
  siblings.billing_state AS right_billing_state,
  siblings.first3_token AS right_first3_token,
  
  p.parent_account_id,
  
  'token_zip' AS "match_type"

FROM parentless ps

JOIN vendor_customers siblings ON
  ps.first3_token = siblings.first3_token
  AND ps.normalized_billing_zip = siblings.normalized_billing_zip

LEFT JOIN vendor_customer_to_parent_account_map _p ON
  siblings.vendor_customer_id = _p.vendor_customer_id

LEFT JOIN parent_accounts p ON
  _p.parent_account_id = p.parent_account_id


WHERE 
  ps.vendor_customer_id <> siblings.vendor_customer_id

), 

potential_siblings_token_only AS (
SELECT
  ps.vendor_customer_id AS left_vendor_customer_id,
  ps.vendor_name AS left_vendor_name,
  ps.raw_vendor_customer_name AS left_raw_vendor_customer_name,
  ps.normalized_vendor_customer_name AS left_normalized_vendor_customer_name,
  ps.normalized_billing_zip AS left_normalized_billing_zip,
  ps.billing_state AS left_billing_state,
  ps.first3_token AS left_first3_token,

  siblings.vendor_customer_id AS right_vendor_customer_id,
  siblings.vendor_name AS right_vendor_name,
  siblings.raw_vendor_customer_name AS right_raw_vendor_customer_name,
  siblings.normalized_vendor_customer_name AS right_normalized_vendor_customer_name,
  siblings.normalized_billing_zip AS right_normalized_billing_zip,
  siblings.billing_state AS right_billing_state,
  siblings.first3_token AS right_first3_token,

  p.parent_account_id,
  
  'token_only' AS "match_type"
FROM parentless ps

JOIN vendor_customers siblings ON
  ps.first3_token = siblings.first3_token

LEFT JOIN vendor_customer_to_parent_account_map _p ON
  siblings.vendor_customer_id = _p.vendor_customer_id

LEFT JOIN parent_accounts p ON
  _p.parent_account_id = p.parent_account_id

WHERE 
  ps.vendor_customer_id <> siblings.vendor_customer_id
  AND NOT EXISTS (
    SELECT 1 
    FROM potential_siblings_token_and_zip matched
    WHERE ps.vendor_customer_id = matched.left_vendor_customer_id
    AND siblings.vendor_customer_id = matched.right_vendor_customer_id
  )
), 

unioned AS (
SELECT * FROM potential_siblings_token_and_zip

UNION

SELECT * FROM potential_siblings_token_only

)
SELECT * FROM unioned
ORDER BY match_type DESC, left_vendor_customer_id ASC 
);






CREATE OR REPLACE VIEW vendor_customer_to_parent_suggestions AS (
WITH parentless AS (
SELECT
  v.vendor_customer_id,
  v.vendor_name,
  v.raw_vendor_customer_name,
  v.normalized_vendor_customer_name,
  v.raw_billing_zip,
  v.normalized_billing_zip,
  v.billing_state,
  v.period_date,
  v.first3_token
FROM vendor_customers v
WHERE NOT EXISTS (
  SELECT 1 
  FROM vendor_customer_to_parent_account_map accepted
  WHERE v.vendor_customer_id = accepted.vendor_customer_id
  )
), potential_parent AS (
SELECT
  pl.vendor_customer_id,
  pl.vendor_name,
  pl.raw_vendor_customer_name,
  pl.normalized_vendor_customer_name,
  pl.raw_billing_zip,
  pl.normalized_billing_zip,
  pl.billing_state,
  pl.period_date,
  pl.first3_token,
  p.parent_account_id,
  p.parent_account_name,
  p.normalized_parent_name
FROM parentless pl
JOIN parent_accounts p ON
  pl.first3_token = p.first3_token
), not_rejected AS (
SELECT
  pp.vendor_customer_id,
  pp.vendor_name,
  pp.raw_vendor_customer_name,
  pp.normalized_vendor_customer_name,
  pp.raw_billing_zip,
  pp.normalized_billing_zip,
  pp.billing_state,
  pp.period_date,
  pp.first3_token,
  pp.parent_account_id,
  pp.parent_account_name,
  pp.normalized_parent_name
FROM potential_parent pp
WHERE NOT EXISTS (
  SELECT 1 
  FROM mismatch_vendor_customer_to_parent_account_map rejected
  WHERE pp.vendor_customer_id = rejected.vendor_customer_id
  AND pp.parent_account_id = rejected.parent_account_id
  )
ORDER BY pp.vendor_customer_id ASC
) 
SELECT 
  * 
FROM not_rejected
);

CREATE OR REPLACE VIEW vendor_customers_vw AS (
SELECT
  v.vendor_customer_id,
  v.vendor_name,
  v.raw_vendor_customer_name,
  v.normalized_vendor_customer_name,
  v.raw_billing_zip,
  v.normalized_billing_zip,
  v.billing_state,
  v.period_date,
  v.first3_token,
  p.parent_account_id,
  p.parent_account_name
FROM vendor_customers v
LEFT JOIN vendor_customer_to_parent_account_map _p ON
  v.vendor_customer_id = _p.vendor_customer_id

LEFT JOIN parent_accounts p ON
  _p.parent_account_id = p.parent_account_id

)