-- A is a sibling of B, therefore B is a sibling of A --
CREATE OR REPLACE VIEW normalized_siblings AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS sibling_source
FROM vendor_siblings

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS sibling_source
FROM vendor_siblings
); 

-- A is a sibling of B, B rejected parent C, A has not rejected C
-- view suggests A may reject C 
CREATE OR REPLACE VIEW inferred_parent_rejections AS (
SELECT
  base.left_vendor_customer_id AS vendor_customer_id,
  base.right_vendor_customer_id AS source_vendor_customer_id,
  rejected.parent_account_id AS parent_account_id
FROM normalized_siblings base
JOIN mismatch_vendor_customer_to_parent_account_map rejected ON
  base.right_vendor_customer_id = rejected.vendor_customer_id
);

-- ============================================================================
-- ================= VENDOR CUSTOMER TO PARENT SUGGESTIONS ====================
-- ============================================================================

-- A is a sibling of B, A does not have a parent, B has parent C, 
-- view suggests 'A is a child of C'
CREATE OR REPLACE VIEW vendor_customer_sibling_parent_inferred AS (
SELECT
  left_vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id AS parent_account_id,
  'sibling_parent_inferred' AS suggestion_type
FROM normalized_siblings base

JOIN vendor_customer_to_parent_account_map right_parent ON
  base.right_vendor_customer_id = right_parent.vendor_customer_id

WHERE 
  NOT EXISTS (
    SELECT 1
    FROM vendor_customer_to_parent_account_map accepted_parents
    WHERE base.left_vendor_customer_id = accepted_parents.vendor_customer_id 
  )
);

-- A has no parent, A has a token and zip that match B, B has a parent C
-- suggest A is a child C 
CREATE OR REPLACE VIEW vendor_customer_token_zip_parent_inferred AS (
SELECT
  base.vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id AS parent_account_id,
  'token_zip_parent_inferred' AS suggestion_type
FROM vendor_customers base

JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token
  AND base.normalized_billing_zip = right_vc.normalized_billing_zip

JOIN vendor_customer_to_parent_account_map right_parent ON
  right_vc.vendor_customer_id = right_parent.vendor_customer_id 

WHERE 
  NOT EXISTS (
    SELECT 1 
    FROM vendor_customer_to_parent_account_map accepted
    WHERE base.vendor_customer_id = accepted.vendor_customer_id
  )

  AND base.vendor_customer_id <> right_vc.vendor_customer_id
);

-- A has no parent, A has a token that matches B, B has a parent C
-- suggest A is a child C 
CREATE OR REPLACE VIEW vendor_customer_token_parent_inferred AS (
SELECT
  base.vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id AS parent_account_id,
  'token_parent_inferred' AS suggestion_type
FROM vendor_customers base

JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token

JOIN vendor_customer_to_parent_account_map right_parent ON
  right_vc.vendor_customer_id = right_parent.vendor_customer_id 

WHERE 
  NOT EXISTS (
    SELECT 1 
    FROM vendor_customer_to_parent_account_map accepted
    WHERE base.vendor_customer_id = accepted.vendor_customer_id
  )

  AND base.vendor_customer_id <> right_vc.vendor_customer_id
);

-- A has no parent, A has a zip that matches B, B has a parent C
-- suggest A is a child C 
CREATE OR REPLACE VIEW vendor_customer_zip_parent_inferred AS (
SELECT
  base.vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id AS parent_account_id,
  'zip_parent_inferred' AS suggestion_type
FROM vendor_customers base

JOIN vendor_customers right_vc ON
  base.normalized_billing_zip = right_vc.normalized_billing_zip

JOIN vendor_customer_to_parent_account_map right_parent ON
  right_vc.vendor_customer_id = right_parent.vendor_customer_id 

WHERE 
  NOT EXISTS (
    SELECT 1 
    FROM vendor_customer_to_parent_account_map accepted
    WHERE base.vendor_customer_id = accepted.vendor_customer_id
  )

  AND base.vendor_customer_id <> right_vc.vendor_customer_id
);

-- inferred and actual rejections for simplified exlusion of all
CREATE OR REPLACE VIEW effective_rejections AS (
SELECT 
  vendor_customer_id,
  parent_account_id
FROM inferred_parent_rejections

UNION

SELECT 
  vendor_customer_id,
  parent_account_id
FROM mismatch_vendor_customer_to_parent_account_map

);

-- all suggestions not yet rejected
CREATE OR REPLACE VIEW vendor_customer_to_parent_suggestions AS (
WITH stacked AS (
SELECT * FROM vendor_customer_sibling_parent_inferred
UNION
SELECT * FROM vendor_customer_token_zip_parent_inferred
UNION
SELECT * FROM vendor_customer_token_parent_inferred
UNION
SELECT * FROM vendor_customer_zip_parent_inferred
)
SELECT
  vendor_customer_id,
  parent_account_id,
  suggestion_type
FROM stacked base
WHERE 
  NOT EXISTS (
    SELECT 1
    FROM effective_rejections rejected
    WHERE base.vendor_customer_id = rejected.vendor_customer_id
    AND base.parent_account_id = rejected.parent_account_id
  )
);
