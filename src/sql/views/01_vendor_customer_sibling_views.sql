-- ======================================================
-- ======= relationship layer for vendor customers ======
-- ======================================================

-- ================== ACCEPTED ===========================
-- A is a sibling of B, therefore B is a sibling of A
CREATE OR REPLACE VIEW normalized_vendor_customer_sibling_map AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS sibling_source,
  NULL AS source
FROM vendor_customer_sibling_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS sibling_source,
  NULL AS source
FROM vendor_customer_sibling_map
); 

-- A rejected B, therefore B rejected A
CREATE OR REPLACE VIEW rejected_normalized_vendor_customer_sibling_map AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  'direct' AS rejection_type,
  NULL AS source_vendor_customer_id
FROM rejected_vendor_customer_sibling_map

UNION

SELECT
  right_vendor_customer_id AS left_vendor_customer_id,
  left_vendor_customer_id AS right_vendor_customer_id,
  'reversed' AS rejection_type,
  NULL AS source_vendor_customer_id
FROM rejected_vendor_customer_sibling_map
);

-- A is a sibling of B, B rejected C, A might reject C, but has not yet
CREATE OR REPLACE VIEW rejected_vendor_customer_sibling_inferred_map AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  source.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS rejection_type,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM normalized_vendor_customer_sibling_map base

JOIN rejected_normalized_vendor_customer_sibling_map source ON
  base.right_vendor_customer_id = source.left_vendor_customer_id

WHERE NOT EXISTS (
  SELECT 1
  FROM rejected_normalized_vendor_customer_sibling_map rejected
  WHERE 
    rejected.left_vendor_customer_id = base.left_vendor_customer_id
    AND rejected.right_vendor_customer_id = source.right_vendor_customer_id
  )
  AND base.left_vendor_customer_id <> source.right_vendor_customer_id
);

-- all vendor customer sibling rejections [Direct, Reversed, Inferred]
CREATE OR REPLACE VIEW effective_vendor_customer_sibling_reject_map AS (
SELECT * FROM rejected_normalized_vendor_customer_sibling_map
UNION ALL
SELECT * FROM rejected_vendor_customer_sibling_inferred_map
);

-- A is a sibling of B, B accepted C, A might accept C, but has not yet
CREATE OR REPLACE VIEW vendor_customer_sibling_inferred_map AS (
SELECT
  base.left_vendor_customer_id AS left_vendor_customer_id,
  source.right_vendor_customer_id AS right_vendor_customer_id,
  'sibling_inferred' AS sibling_source,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM normalized_vendor_customer_sibling_map base

JOIN normalized_vendor_customer_sibling_map source ON
  base.right_vendor_customer_id = source.left_vendor_customer_id

WHERE 
  NOT EXISTS (
    SELECT 1
    FROM normalized_vendor_customer_sibling_map accepted
    WHERE 
      accepted.left_vendor_customer_id = base.left_vendor_customer_id
      AND accepted.right_vendor_customer_id = source.right_vendor_customer_id
  )
  AND base.left_vendor_customer_id <> source.right_vendor_customer_id
);

-- All vendor customer siblings, [Direct, Reversed, Inferred]
CREATE OR REPLACE VIEW effective_vendor_customer_sibling_map AS (
SELECT * FROM normalized_vendor_customer_sibling_map
UNION ALL
SELECT * FROM vendor_customer_sibling_inferred_map
);