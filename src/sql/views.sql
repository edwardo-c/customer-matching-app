CREATE OR REPLACE VIEW vendor_customer_to_erp_account_candidate_vw AS (
SELECT
  base.vendor_customer_id,
  base.erp_account_id,
  base.score,
  base.status
FROM vendor_customer_to_erp_account_candidate_map base
)


-- CREATE OR REPLACE VIEW workflow_vendor_customers_mapping_vw AS (
-- SELECT
--   base.vendor_customer_id,
--   base.vendor_name,
--   base.raw_vendor_customer_name,
--   base.normalized_vendor_customer_name,
--   base.vendor_customer_billing_zip,
--   base.vendor_customer_billing_state,
--   base.vendor_customer_billing_city,
--   base.vendor_customer_first3_token,
--   e.erp_account_id,
--   e.erp_account_number,
--   e.erp_account_name,
--   e.erp_name_first3_token,
--   p.parent_account_name
-- FROM vendor_customers base
-- -- show erp mapping if exists
-- LEFT JOIN vendor_customer_to_erp_account_map v2e_map ON
--   base.vendor_customer_id = v2e_map.vendor_customer_id
-- LEFT JOIN erp_accounts e ON
--   v2e_map.erp_account_id = e.erp_account_id
-- -- show parent mapping if exists
-- LEFT JOIN vendor_customer_to_parent_account_map v2p_map ON 
--   base.vendor_customer_id = v2p_map.vendor_customer_id
-- LEFT JOIN parent_accounts p ON
--   v2p_map.parent_account_id = p.parent_account_id
-- );

-- CREATE OR REPLACE VIEW workflow_erp_accounts_vw AS (
-- SELECT
--   base.erp_account_id,
--   base.erp_account_number,
--   base.erp_account_name,
--   base.normalized_erp_account_name,
--   base.erp_account_billing_zip,
--   base.erp_account_billing_state,
--   base.erp_account_billing_city,
--   base.erp_name_first3_token,
--   p.parent_account_id,
--   p.parent_account_name
-- FROM erp_accounts base
-- LEFT JOIN erp_account_to_parent_account_map e2p_map ON
--   base.erp_account_id = e2p_map.erp_account_id
-- LEFT JOIN parent_accounts p ON 
--   e2p_map.parent_account_id = p.parent_account_id
-- );


