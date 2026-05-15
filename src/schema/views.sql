-- every vendor customer mapped to an erp customer
CREATE OR REPLACE VIEW vendor_cust_to_erp_cust_vw AS (
SELECT 
  erp.erp_account_number,
  erp.erp_account_name,
  vc.vendor_name,
  vc.raw_vendor_customer_name,
  vc.normalized_customer_name
FROM vendor_customer_to_erp_acct_map b
JOIN erp_accounts erp ON
  b.erp_account_id = erp.erp_account_id
JOIN vendor_customers vc ON
  b.erp_account_id = vc.vendor_customer_id
);


-- every vendor customer mapped to a parent
CREATE OR REPLACE VIEW vendor_cust_to_parent_vw AS (
SELECT 
  p.parent_account_name,
  p.normalized_parent_name,
  vc.vendor_name,
  vc.raw_vendor_customer_name,
  vc.normalized_customer_name
FROM vendor_customer_to_parent_account_map b
JOIN parent_accounts p ON
  b.parent_account_id = p.parent_account_id
JOIN vendor_customers vc ON
  b.vendor_customer_id = vc.vendor_customer_id
);


-- TODO: every erp customer mapped to a parent
CREATE OR REPLACE VIEW erp_cust_to_parent_vw AS (
SELECT 
  p.parent_account_name,
  p.normalized_parent_name,
  erp.erp_account_number,
  erp.erp_account_name
FROM erp_account_to_parent_account_map b
JOIN parent_accounts p ON
  b.parent_account_id = p.parent_account_id
JOIN erp_accounts erp ON
  b.erp_account_id = erp.erp_account_id
);


-- TODO: CREATE OR REPLACE VIEW all_relationships AS ();
