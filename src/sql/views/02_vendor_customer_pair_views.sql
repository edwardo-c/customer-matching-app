-- =================================================
-- ======= relationship/candidate-pair layer. ======
-- =================================================


-- vendor customers ===============================
-- A is a sibling of B, therefore B is a sibling of A
CREATE OR REPLACE VIEW accepted_normalized_vendor_customer_sibling_map AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS sibling_source
FROM accepted_vendor_siblings_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS sibling_source
FROM accepted_vendor_siblings_map
); 

-- A rejected B, therefore B rejected A
CREATE OR REPLACE VIEW rejected_normalized_vendor_customer_sibling_map AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS rejection_type
FROM rejected_vendor_customer_sibling_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS rejection_type
FROM rejected_vendor_customer_sibling_map
);

-- A is a sibling of B, B rejected C, A might reject C
CREATE OR REPLACE VIEW rejected_vendor_customer_sibling_inferred AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  rejected.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS rejection_type,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM accepted_normalized_vendor_customer_sibling_map base
JOIN rejected_normalized_vendor_customer_sibling_map rejected ON
  base.right_vendor_customer_id = rejected.left_vendor_customer_id
);

-- compiled rejections for simplified comparison, inferred and direct
CREATE OR REPLACE VIEW rejected_effective_vendor_customer_sibling_map AS (
WITH stacked AS (
  -- direct rejected sibling pairs, already normalized both directions
  SELECT
    left_vendor_customer_id,
    right_vendor_customer_id,
    rejection_type,
  FROM rejected_normalized_vendor_customer_sibling_map

  UNION ALL

  -- inferred rejected sibling pairs from confirmed siblings
  SELECT
    left_vendor_customer_id,
    right_vendor_customer_id,
    rejection_type
  FROM rejected_vendor_customer_sibling_inferred
)

SELECT DISTINCT
  left_vendor_customer_id,
  right_vendor_customer_id,
  rejection_type
FROM stacked
);

-- A is a sibling of B, B is a sibling of C, A might be a sibling of C
CREATE OR REPLACE VIEW vendor_customer_sibling_inferred_candidate_map AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  siblings.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS suggestion_type,
  1 as priority,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM accepted_normalized_vendor_customer_sibling_map base
JOIN accepted_normalized_vendor_customer_sibling_map siblings ON
  base.right_vendor_customer_id = siblings.left_vendor_customer_id
);

-- vendor customer A has a token and zip that match vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_token_zip_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'token_zip' AS suggestion_type,
  2 AS priority,
  NULL as source_vendor_customer_id
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token
  AND base.normalized_billing_zip = right_vc.normalized_billing_zip
);

-- vendor customer A has a zip that matches vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_zip_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'zip' AS suggestion_type,
  3 AS priority,
  NULL as source_vendor_customer_id
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.normalized_billing_zip = right_vc.normalized_billing_zip
);

-- vendor customer A has a token that matches vendor customer B
CREATE OR REPLACE VIEW parentless_vendor_customer_token_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  right_vc.vendor_customer_id AS right_vendor_customer_id,
  'token' AS suggestion_type,
  4 AS priority,
  NULL as source_vendor_customer_id
FROM parentless_vendor_customers base
JOIN vendor_customers right_vc ON
  base.first3_token = right_vc.first3_token
);

-- similar token/zip, token, and zip
CREATE OR REPLACE VIEW vendor_customer_candidate_sibling_map AS (
WITH stacked AS (
SELECT * FROM vendor_customer_sibling_inferred_candidate_map

UNION ALL

SELECT * FROM parentless_vendor_customer_token_zip_candidate_map

UNION ALL

SELECT * FROM parentless_vendor_customer_token_candidate_map

UNION ALL

SELECT * FROM parentless_vendor_customer_zip_candidate_map
), filtered AS (
SELECT
  base.left_vendor_customer_id,
  base.right_vendor_customer_id,
  base.suggestion_type,
  base.priority,
  base.source_vendor_customer_id
FROM stacked base
WHERE 
  base.left_vendor_customer_id <> base.right_vendor_customer_id

  -- pair has not been excluded by the direct/inferred rejection map
  AND NOT EXISTS (
    SELECT 1
    FROM rejected_effective_vendor_customer_sibling_map rejected
    WHERE base.left_vendor_customer_id = rejected.left_vendor_customer_id
    AND base.right_vendor_customer_id = rejected.right_vendor_customer_id
  )

  -- pair is not an already confirmed as siblings
  AND NOT EXISTS (
    SELECT 1
    FROM accepted_normalized_vendor_customer_sibling_map accepted
    WHERE base.left_vendor_customer_id = accepted.left_vendor_customer_id
      AND base.right_vendor_customer_id = accepted.right_vendor_customer_id
  )
), ranked AS (
SELECT
  -- rank highest grouping by highest priority
  base.*,
  ROW_NUMBER() OVER (
    PARTITION BY base.left_vendor_customer_id, base.right_vendor_customer_id
    ORDER BY base.priority ASC
  ) AS rn
FROM filtered base
)
-- return only the highest priority pairing for each group
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  suggestion_type,
  priority,
  source_vendor_customer_id
FROM ranked 
WHERE rn = 1
);

-- erp accounts ===============================
-- 