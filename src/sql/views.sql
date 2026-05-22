CREATE OR REPLACE VIEW vendor_customer_to_erp_account_candidate_vw AS (
SELECT
  base.vendor_customer_id,
  base.erp_account_id,
  base.score,
  base.status
FROM vendor_customer_to_erp_account_candidate_map base
);

CREATE OR REPLACE VIEW suggested_vendor_customer_parents_vw AS (
WITH base AS (SELECT DISTINCT
  vendor_customer_first3_token AS first3_token,
  vendor_customer_billing_state AS state,
  vendor_customer_billing_zip AS zip,
  COUNT(vendor_customer_id) AS count_of_potential_siblings
FROM vendor_customers
GROUP BY ALL
HAVING COUNT(vendor_customer_id) > 1
), potential_parents AS (
SELECT 
  COUNT(parent_account_id) AS count_of_parents_with_same_token,
  parent_name_first3_token AS first3_token
FROM parent_accounts
GROUP BY ALL
) 
SELECT
  b.first3_token,
  b.state,
  b.zip,
  b.count_of_potential_siblings,
  COALESCE(p.count_of_parents_with_same_token, 0) AS count_of_parents_with_same_token
FROM base b
LEFT JOIN potential_parents p ON
  b.first3_token = p.first3_token
);



