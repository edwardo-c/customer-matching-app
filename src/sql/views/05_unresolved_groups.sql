-- A, B, and C all look related, but none have a parent
CREATE OR REPLACE VIEW parentless_vendor_customer_groups AS (
WITH base AS (
-- with all parentless vendor customers
SELECT
  vendor_customer_id,
  normalized_billing_zip,
  first3_token
FROM parentless_vendor_customers
), ranked AS (
SELECT
  b.*,
  -- generate a group id for each billing zip / token combo
  DENSE_RANK() OVER (
    ORDER BY normalized_billing_zip, first3_token
  ) AS unresolved_group,

  -- count number of candidates per group
  COUNT(*) OVER (
    PARTITION BY normalized_billing_zip, first3_token
  ) AS candidate_count
FROM base b
)
-- return only groups that have candidates > 1
SELECT  
  vendor_customer_id,
  normalized_billing_zip,
  first3_token,
  'token_zip' AS group_type
FROM ranked WHERE candidate_count > 1
);