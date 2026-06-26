-- ===== Vendor customer to Erp Relationships =========

-- vendor customer A is a sibling of vendor customer B, vendor customer B rejected ERP account C
-- supress suggesting vendor customer A to erp account C
CREATE OR REPLACE VIEW effective_rejected_vendor_customer_to_erp_account_map AS (
WITH stacked AS (
SELECT
  base.vendor_customer_id,
  base.erp_account_id,
  NULL AS source_vendor_customer_id,
  'direct' AS rejection_type
FROM rejected_vendor_customer_to_erp_account_map base

UNION

SELECT
  siblings.left_vendor_customer_id AS vendor_customer_id,
  rejected.erp_account_id,
  siblings.right_vendor_customer_id AS source_vendor_customer_id,
  'sibling_inferred' AS rejection_type
FROM accepted_normalized_vendor_customer_sibling_map siblings

JOIN rejected_vendor_customer_to_erp_account_map rejected ON
 siblings.right_vendor_customer_id = rejected.vendor_customer_id
)
-- TODO: Seperate into debug views - this will still have dupes even with DISTINCT
SELECT DISTINCT
  vendor_customer_id,
  erp_account_id,
  source_vendor_customer_id,
  rejection_type
FROM stacked
);

-- vendor customer A is not linked to an erp account
-- vendor customer A is a sibling of vendor customer B
-- vendor customer B is linked to erp account C
-- view suggests vendor customer A might be linked to erp account C
CREATE OR REPLACE VIEW erpless_vendor_customer_to_erp_account_sibling_inferred_map AS (
SELECT
  base.vendor_customer_id,
  accepted.erp_account_id,
  siblings.right_vendor_customer_id AS source_vendor_customer_id,
  'sibling_inferred' AS suggestion_type,
  1 AS priority
FROM erpless_vendor_customers base

JOIN accepted_normalized_vendor_customer_sibling_map siblings ON
    base.vendor_customer_id = siblings.left_vendor_customer_id

JOIN accepted_vendor_customer_to_erp_account_map accepted ON
    accepted.vendor_customer_id = siblings.right_vendor_customer_id
);

-- vendor customer A shares a token and zip that match erp account B
CREATE OR REPLACE VIEW erpless_vendor_customers_to_erp_account_token_zip_candidate_map AS (
SELECT
  vendor_customer_id,
  erp.erp_account_id,
  'token_zip' AS suggestion_type,
  2 AS priority
FROM erpless_vendor_customers base
JOIN erp_accounts erp ON
  base.normalized_billing_zip = erp.normalized_billing_zip
  AND base.first3_token = erp.first3_token
);

-- vendor customer A shares a zip that matches erp account B
CREATE OR REPLACE VIEW erpless_vendor_customers_to_erp_account_zip_candidate_map AS (
SELECT
  vendor_customer_id,
  erp.erp_account_id,
  'zip' AS suggestion_type,
  3 AS priority
FROM erpless_vendor_customers base
JOIN erp_accounts erp ON
  base.normalized_billing_zip = erp.normalized_billing_zip
);

-- vendor customer A shares a token that matches erp account B
CREATE OR REPLACE VIEW erpless_vendor_customers_to_erp_account_token_candidate_map AS (
SELECT
  vendor_customer_id,
  erp.erp_account_id,
  'token' AS suggestion_type,
  4 AS priority
FROM erpless_vendor_customers base
JOIN erp_accounts erp ON
  base.first3_token = erp.first3_token
);

CREATE OR REPLACE VIEW erpless_vendor_customer_to_erp_account_candidate_map AS (
WITH stacked AS (
SELECT 
  vendor_customer_id,
  erp_account_id,
  suggestion_type,
  priority
FROM erpless_vendor_customer_to_erp_account_sibling_inferred_map

UNION ALL

SELECT * FROM erpless_vendor_customers_to_erp_account_token_zip_candidate_map

UNION ALL

SELECT * FROM erpless_vendor_customers_to_erp_account_zip_candidate_map

UNION ALL

SELECT * FROM erpless_vendor_customers_to_erp_account_token_candidate_map

), filtered AS (
SELECT
*
FROM stacked s
-- candidates not excluded yet (direct or inferred)
WHERE 
  NOT EXISTS (
    SELECT 1
    FROM effective_rejected_vendor_customer_to_erp_account_map rejected
    WHERE s.vendor_customer_id = rejected.vendor_customer_id
    AND s.erp_account_id = rejected.erp_account_id
  )
-- candidates not already confirmed
  AND NOT EXISTS (
    SELECT 1
    FROM accepted_vendor_customer_to_erp_account_map accepted
    WHERE s.vendor_customer_id = accepted.vendor_customer_id
    AND s.erp_account_id = accepted.erp_account_id
  )
), ranked AS (
SELECT 
  f.*,
  ROW_NUMBER() OVER (
    PARTITION BY f.vendor_customer_id, f.erp_account_id
    ORDER BY priority ASC
  ) AS rn
FROM filtered f
)
SELECT
  vendor_customer_id,
  erp_account_id,
  suggestion_type,
  priority
FROM ranked
WHERE rn = 1
);