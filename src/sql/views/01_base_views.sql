-- ===============================================================
-- ============= Anything reused by multiple workflows ===========
-- ===============================================================

-- vendor customers not connected to a parent account
CREATE OR REPLACE VIEW parentless_vendor_customers AS (
SELECT
  base.vendor_customer_id,
  base.normalized_billing_zip,
  base.first3_token
FROM vendor_customers base
WHERE NOT EXISTS (
  SELECT 1
  FROM accepted_vendor_customer_to_parent_account_map accepted
  WHERE base.vendor_customer_id = accepted.vendor_customer_id 
  )
);

-- vendor customers not connected to an erp account
CREATE OR REPLACE VIEW erpless_vendor_customers AS (
SELECT
  base.vendor_customer_id,
  base.normalized_billing_zip,
  base.first3_token
FROM vendor_customers base
WHERE NOT EXISTS (
  SELECT 1
  FROM accepted_vendor_customer_to_erp_account_map accepted
  WHERE base.vendor_customer_id = accepted.vendor_customer_id 
  )
);

-- A is a sibling of B, therefore B is a sibling of A
CREATE OR REPLACE VIEW accepted_normalized_vendor_customer_sibling_map AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS sibling_source
FROM accepted_vendor_customer_sibling_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS sibling_source
FROM accepted_vendor_customer_sibling_map
); 

-- ================ NOT USED YET ================


-- erp accounts not connected to a parent account
CREATE OR REPLACE VIEW parentless_erp_accounts AS (
SELECT
  base.erp_account_id,
  base.normalized_billing_zip,
  base.first3_token
FROM erp_accounts base
WHERE NOT EXISTS (
  SELECT 1
  FROM accepted_erp_account_to_parent_account_map accepted
  WHERE base.vendor_customer_id = accepted.vendor_customer_id 
  )
);