-- A is a sibling of B, therefore B is a sibling of A
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

CREATE OR REPLACE VIEW normalized_vendor_customer_sibling_mismatches AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS mismatch_source
FROM vendor_customer_sibling_mismatch_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS mismatch_source
FROM vendor_customer_sibling_mismatch_map
);

-- A is a sibling of B, B rejected C, A might reject C
CREATE OR REPLACE VIEW vendor_customer_rejected_siblings_inferred AS (
SELECT
  left_vendor_customer_id AS left_vendor_customer_id,
  rejected.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS rejection_type
FROM normalized_siblings base
JOIN normalized_vendor_customer_sibling_mismatches rejected ON
  base.right_vendor_customer_id = rejected.left_vendor_customer_id
);

-- compiled rejections for efficient/simplified comparison
CREATE OR REPLACE VIEW effective_vendor_siblings_rejection AS (
WITH stacked AS (
  -- direct rejected sibling pairs, already normalized both directions
  SELECT
    left_vendor_customer_id,
    right_vendor_customer_id
  FROM normalized_vendor_customer_sibling_mismatches

  UNION ALL

  -- inferred rejected sibling pairs from confirmed siblings
  SELECT
    left_vendor_customer_id,
    right_vendor_customer_id
  FROM vendor_customer_rejected_siblings_inferred
)

SELECT DISTINCT
  left_vendor_customer_id,
  right_vendor_customer_id
FROM stacked
);

-- A is a sibling of B, B is a sibling of C, A might be a sibling of C
CREATE OR REPLACE VIEW vendor_customer_sibling_inferred_candidates AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  siblings.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS suggestion_type,
  1 as priority
FROM normalized_siblings base
JOIN normalized_siblings siblings ON
  base.right_vendor_customer_id = siblings.left_vendor_customer_id
);

-- vendor customers in need of a parent (parentless)
CREATE OR REPLACE VIEW parentless_vendor_customers AS (
SELECT
  base.vendor_customer_id,
  base.normalized_billing_zip,
  base.first3_token
FROM vendor_customers base
WHERE NOT EXISTS (
  SELECT 1
  FROM vendor_customer_to_parent_account_map accepted_parents
  WHERE base.vendor_customer_id = accepted_parents.vendor_customer_id 
  )
);

-- vendor customer A has a token and zip that match vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_token_zip_candidates AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'token_zip' AS suggestion_type,
  2 AS priority
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token
  AND base.normalized_billing_zip = right_vc.normalized_billing_zip
);

-- vendor customer A has a zip that matches vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_zip_candidates AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'zip' AS suggestion_type,
  3 AS priority
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.normalized_billing_zip = right_vc.normalized_billing_zip
);

-- vendor customer A has a token that matches vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_token_candidates AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'token' AS suggestion_type,
  4 AS priority
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token
);

-- The vendor customer pairs worth inspecting
-- similar token/zip, token, and zip
CREATE OR REPLACE VIEW vendor_customer_candidate_siblings AS (
WITH stacked AS (
SELECT * FROM vendor_customer_sibling_inferred_candidates

UNION ALL

SELECT * FROM parentless_vendor_customer_token_zip_candidates

UNION ALL

SELECT * FROM parentless_vendor_customer_token_candidates

UNION ALL

SELECT * FROM parentless_vendor_customer_zip_candidates
), filtered AS (
SELECT
  base.left_vendor_customer_id,
  base.right_vendor_customer_id,
  base.suggestion_type,
  base.priority
FROM stacked base
WHERE 
  left_vendor_customer_id <> right_vendor_customer_id

  AND NOT EXISTS (
    SELECT 1
    FROM effective_vendor_siblings_rejection rejected
    WHERE base.left_vendor_customer_id = rejected.left_vendor_customer_id
    AND base.right_vendor_customer_id = rejected.right_vendor_customer_id
  )

  AND NOT EXISTS (
    SELECT 1
    FROM normalized_siblings accepted
    WHERE base.left_vendor_customer_id = accepted.left_vendor_customer_id
      AND base.right_vendor_customer_id = accepted.right_vendor_customer_id
  )
), ranked AS (
SELECT
  base.*,
  ROW_NUMBER() OVER (
    PARTITION BY base.left_vendor_customer_id, base.right_vendor_customer_id
    ORDER BY base.priority ASC
  ) AS rn
FROM filtered base
)
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  suggestion_type,
  priority
FROM ranked 
WHERE rn = 1
);

-- A is a sibling of B, B rejected parent C, supress A -> C
CREATE OR REPLACE VIEW effective_vendor_customer_to_parent_rejections AS (
-- inferred rejections
SELECT
  left_vendor_customer_id AS vendor_customer_id,
  rejected.parent_account_id AS parent_account_id,
  'sibling_inferred' AS rejection_type,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM normalized_siblings base
JOIN mismatch_vendor_customer_to_parent_account_map rejected ON
  base.right_vendor_customer_id = rejected.vendor_customer_id

UNION

-- original rejections
SELECT
  vendor_customer_id,
  parent_account_id,
  'direct_rejection' AS rejection_type
  NULL AS source_vendor_customer_id
FROM mismatch_vendor_customer_to_parent_account_map
);

-- candidate pairs, A is parentless, B has a parent, should A roll up to B's parent?
CREATE OR REPLACE VIEW suggested_parents AS (
WITH filtered AS (
SELECT 
  base.left_vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id,
  base.suggestion_type,
  base.priority
FROM vendor_customer_candidate_siblings base
JOIN vendor_customer_to_parent_account_map right_parent ON
  base.right_vendor_customer_id = right_parent.vendor_customer_id

-- exclude inferred and direct mismatches
WHERE 
  NOT EXISTS (
    SELECT 1
    FROM effective_vendor_customer_to_parent_rejections rejected
    WHERE base.left_vendor_customer_id = rejected.vendor_customer_id
    AND right_parent.parent_account_id = rejected.parent_account_id
  )
  
  AND NOT EXISTS (
    SELECT 1
    FROM vendor_customer_to_parent_account_map accepted
    WHERE base.left_vendor_customer_id = accepted.vendor_customer_id
  )

), ranked AS (
SELECT 
  base.*,
  ROW_NUMBER() OVER (
    PARTITION BY base.vendor_customer_id, base.parent_account_id
    ORDER BY priority ASC
  ) AS rn
FROM filtered base
) 
SELECT 
  vendor_customer_id,
  parent_account_id,
  suggestion_type,
  priority
FROM ranked
WHERE rn = 1
);

