CREATE OR REPLACE VIEW vendor_customer_sibling_candidates_ui AS (
WITH normalized_ids AS (
SELECT
  GREATEST(
    base.left_vendor_customer_id, 
    base.right_vendor_customer_id
  ) AS greatest_vendor_customer_id,

  LEAST(
    base.left_vendor_customer_id, 
    base.right_vendor_customer_id
  ) AS least_vendor_customer_id

FROM vendor_customer_candidate_sibling_map base
), deduped AS (
SELECT DISTINCT
  greatest_vendor_customer_id AS left_vendor_customer_id,
  least_vendor_customer_id AS right_vendor_customer_id
FROM normalized_ids
)
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  left_meta.vendor_name AS left_vendor_name,
  left_meta.raw_vendor_customer_name AS left_raw_vendor_customer_name,
  left_meta.billing_state AS left_billing_state,
  left_meta.normalized_billing_zip AS left_normalized_billing_zip,

  base.right_vendor_customer_id AS right_vendor_customer_id,
  right_meta.vendor_name AS right_vendor_name,
  right_meta.raw_vendor_customer_name AS right_raw_vendor_customer_name,
  right_meta.billing_state AS right_billing_state,
  right_meta.normalized_billing_zip AS right_normalized_billing_zip,

  orig.priority AS priority

FROM deduped base

JOIN vendor_customers left_meta ON
  base.left_vendor_customer_id = left_meta.vendor_customer_id

JOIN vendor_customers right_meta ON
  base.right_vendor_customer_id = right_meta.vendor_customer_id

JOIN vendor_customer_candidate_sibling_map orig ON
  base.left_vendor_customer_id = orig.left_vendor_customer_id
  AND base.right_vendor_customer_id = orig.right_vendor_customer_id
);