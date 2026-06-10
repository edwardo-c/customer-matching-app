CREATE OR REPLACE VIEW potential_vendor_siblings AS (
WITH base AS (
SELECT
  vc.vendor_customer_id,
  vc.vendor_name,
  vc.normalized_vendor_customer_name,
  vc.first3_token,
  vc.billing_state,
  vc.billing_zip,
  p.parent_account_name
FROM vendor_customers vc

LEFT JOIN vendor_customer_to_parent_account_map pid ON 
  vc.vendor_customer_id = pid.vendor_customer_id
LEFT JOIN parent_accounts p ON
  pid.parent_account_id = p.parent_account_id

WHERE 
  vc.first3_token IS NOT NULL
  AND vc.billing_state IS NOT NULL
  AND vc.billing_zip IS NOT NULL
), 

counted AS (
SELECT 
  *,
  COUNT(*) OVER (
    PARTITION BY base.first3_token, base.billing_state, base.billing_zip
  ) AS sibling_count
FROM base
), 

filtered as (
  SELECT * FROM counted
WHERE sibling_count > 1
AND parent_account_name IS NULL
), 

ranked AS (
SELECT 
  *,
  DENSE_RANK() OVER (
  PARTITION BY filtered.first3_token, filtered.billing_state, filtered.billing_zip
  ) AS candidate_index
FROM filtered

)
SELECT 
  candidate_index,
  vendor_customer_id,
  parent_account_name,
  vendor_name,
  normalized_vendor_customer_name,
  first3_token,
  billing_state,
  billing_zip
FROM ranked
);

CREATE OR REPLACE VIEW suggested_vendor_parents AS (
SELECT DISTINCT
  base.candidate_index,
  base.first3_token,
  p.parent_account_id,
  p.parent_account_name,
  p.normalized_parent_name
FROM potential_vendor_siblings base
JOIN parent_accounts p ON 
  base.first3_token = p.first3_token
);



-- CREATE OR REPLACE VIEW vendor_to_parent_candidates AS (
-- SELECT
--   vc.vendor_customer_id,
--   vc.vendor_name,
--   vc.raw_vendor_customer_name,
--   vc.normalized_vendor_customer_name,
--   vc.billing_zip,
--   vc.billing_state,
--   vc.billing_city,
--   vc.first3_token AS vendor_first3_token,

--   p.parent_account_id,
--   p.parent_account_name,
--   p.normalized_parent_name,
--   p.first3_token AS parent_first3_token
-- FROM vendor_customers vc
-- INNER JOIN parent_accounts p ON
--   vc.first3_token = p.first3_token
-- WHERE 
--   NOT EXISTS (
--     SELECT 1
--     FROM vendor_customer_to_parent_account_map v2p
--     WHERE vc.vendor_customer_id = v2p.vendor_customer_id
--   )
--   AND NOT EXISTS (
--     SELECT 1
--     FROM mismatch_vendor_customer_to_parent_account_map rejected
--     WHERE vc.vendor_customer_id = rejected.vendor_customer_id
--     AND p.parent_account_id = rejected.parent_account_id
--   )
-- ORDER BY
--   vc.vendor_customer_id,
--   p.parent_account_id
-- );


-- CREATE OR REPLACE VIEW vendor_to_erp_candidates AS (
-- WITH token_state_zip AS (
-- SELECT
--   vc.vendor_customer_id,
--   e.erp_account_id,
--   'token_state_zip' AS match_type
-- FROM vendor_customers vc
-- INNER JOIN erp_accounts e ON
--   vc.first3_token = e.first3_token
--   AND vc.billing_state = e.billing_state
--   AND vc.billing_zip = e.billing_zip
-- WHERE 
--   NOT EXISTS (
--     SELECT 1 
--     FROM vendor_customer_to_erp_account_map accepted
--     WHERE vc.vendor_customer_id = accepted.vendor_customer_id
--   )
--   AND NOT EXISTS (
--     SELECT 1
--     FROM mismatch_vendor_customer_to_erp_account_map rejected
--     WHERE vc.vendor_customer_id = rejected.vendor_customer_id
--     AND e.erp_account_id = rejected.erp_account_id
--   )
-- ), token_state AS (
-- SELECT
--   vc.vendor_customer_id,
--   e.erp_account_id,
--   'token_state' AS match_type
-- FROM vendor_customers vc
-- JOIN erp_accounts e ON
--   vc.first3_token = e.first3_token
--   AND vc.billing_state = e.billing_state
-- WHERE
--   NOT EXISTS (
--     SELECT 1
--     FROM vendor_customer_to_erp_account_map accepted
--     WHERE vc.vendor_customer_id = accepted.vendor_customer_id
--   )
--   AND NOT EXISTS (
--     SELECT 1 
--     FROM mismatch_vendor_customer_to_erp_account_map rejected
--     WHERE vc.vendor_customer_id = rejected.vendor_customer_id
--     AND e.erp_account_id = rejected.erp_account_id
--   )
-- ), token AS (
-- SELECT
--   vc.vendor_customer_id,
--   e.erp_account_id,
--   'token' AS match_type
-- FROM vendor_customers vc
-- JOIN erp_accounts e ON
--   vc.first3_token = e.first3_token
-- WHERE
--   NOT EXISTS (
--     SELECT 1
--     FROM vendor_customer_to_erp_account_map accepted
--     WHERE vc.vendor_customer_id = accepted.vendor_customer_id
--   )
--   AND NOT EXISTS (
--     SELECT 1 
--     FROM mismatch_vendor_customer_to_erp_account_map rejected
--     WHERE vc.vendor_customer_id = rejected.vendor_customer_id
--     AND e.erp_account_id = rejected.erp_account_id
--   )
-- ), unioned AS (
-- SELECT * FROM token_state_zip
-- UNION ALL
-- SELECT * FROM token_state
-- UNION ALL 
-- SELECT * FROM token
-- ) 
-- SELECT
--   base.vendor_customer_id,
--   base.erp_account_id,
--   base.match_type,

--   vc.vendor_name,
--   vc.raw_vendor_customer_name,
--   vc.normalized_vendor_customer_name,
--   vc.billing_zip AS vendor_customer_billing_zip,
--   vc.billing_state AS vendor_customer_billing_state,
--   vc.first3_token AS vendor_customer_first3_token,

--   e.erp_account_number,
--   e.erp_account_name,
--   e.normalized_erp_account_name,
--   e.billing_zip AS erp_billing_zip,
--   e.billing_state AS erp_billing_state,
--   e.first3_token AS erp_first3_token

-- FROM unioned base
-- JOIN vendor_customers vc ON
--   base.vendor_customer_id = vc.vendor_customer_id
-- JOIN erp_accounts e ON 
--   base.erp_account_id = e.erp_account_id
-- ORDER BY 
--   base.match_type DESC,
--   base.vendor_customer_id,
--   base.erp_account_id
-- );
