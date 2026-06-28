CREATE OR REPLACE VIEW vendor_customer_candidates_ui AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  left_meta.vendor_name AS left_vendor_name,
  left_meta.raw_vendor_customer_name AS left_raw_vendor_customer_name,
  left_meta.normalized_billing_zip AS left_normalized_billing_zip,

  base.right_vendor_customer_id AS right_vendor_customer_id,
  right_meta.vendor_name AS right_vendor_name,
  right_meta.raw_vendor_customer_name AS right_raw_vendor_customer_name,
  right_meta.normalized_billing_zip AS right_normalized_billing_zip,

  base.suggestion_type AS suggestion_type,
  base.priority AS priority

FROM vendor_customer_candidate_sibling_map base

JOIN vendor_customers left_meta ON
  base.left_vendor_customer_id = left_meta.vendor_customer_id

JOIN vendor_customers right_meta ON
  base.right_vendor_customer_id = right_meta.vendor_customer_id

);