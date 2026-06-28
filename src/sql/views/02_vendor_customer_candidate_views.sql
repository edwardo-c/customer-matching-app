-- ======================================================
-- ======= candidate layer for vendor customers ======
-- ======================================================

CREATE OR REPLACE VIEW unresolved_vendor_customers AS (
SELECT
  base.vendor_customer_id,
  base.normalized_billing_zip,
  base.first3_token
FROM vendor_customers base
WHERE NOT EXISTS (
  SELECT 1
  FROM vendor_customer_to_resolved_customer_map accepted
  WHERE base.vendor_customer_id = accepted.vendor_customer_id 
  )
);

-- vendor customer A has a token and zip that match vendor customer B
CREATE OR REPLACE VIEW unresolved_vendor_customer_token_zip_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  candidate.vendor_customer_id AS right_vendor_customer_id,
  'token_zip' AS suggestion_type,
  2 AS priority
FROM unresolved_vendor_customers base
JOIN vendor_customers candidate ON
  base.first3_token = candidate.first3_token
  AND base.normalized_billing_zip = candidate.normalized_billing_zip
);

-- vendor customer A has a zip that matches vendor customer B
CREATE OR REPLACE VIEW unresolved_vendor_customer_zip_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  candidate.vendor_customer_id AS right_vendor_customer_id,
  'zip' AS suggestion_type,
  3 AS priority
FROM unresolved_vendor_customers base
JOIN vendor_customers candidate ON
  base.normalized_billing_zip = candidate.normalized_billing_zip
);

-- vendor customer A has a token that matches vendor customer B
CREATE OR REPLACE VIEW unresolved_vendor_customer_token_candidate_map AS (
SELECT
  base.vendor_customer_id AS left_vendor_customer_id,
  candidate.vendor_customer_id AS right_vendor_customer_id,
  'token' AS suggestion_type,
  4 AS priority
FROM unresolved_vendor_customers base
JOIN vendor_customers candidate ON
  base.first3_token = candidate.first3_token
);

-- similar token/zip, token, and zip, and sibling inferred candidates
CREATE OR REPLACE VIEW vendor_customer_candidate_sibling_map AS (
WITH stacked AS (
SELECT
  left_vendor_customer_id,
  right_vendor_customer_id,
  sibling_source AS suggestion_type,
  1 AS priority
FROM vendor_customer_sibling_inferred_map

UNION ALL

SELECT * FROM unresolved_vendor_customer_token_zip_candidate_map

UNION ALL

SELECT * FROM unresolved_vendor_customer_zip_candidate_map

UNION ALL

SELECT * FROM unresolved_vendor_customer_token_candidate_map
), filtered AS (
 
SELECT
  base.left_vendor_customer_id,
  base.right_vendor_customer_id,
  base.suggestion_type,
  base.priority
FROM stacked base
WHERE 
  base.left_vendor_customer_id <> base.right_vendor_customer_id

  -- pair has not been excluded by the direct/inferred rejection map
  AND NOT EXISTS (
    SELECT 1
    FROM effective_vendor_customer_sibling_reject_map rejected
    WHERE base.left_vendor_customer_id = rejected.left_vendor_customer_id
    AND base.right_vendor_customer_id = rejected.right_vendor_customer_id
  )

  -- candidates are not already a confirmed sibling pair
  AND NOT EXISTS (
    SELECT 1
    FROM normalized_vendor_customer_sibling_map accepted
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

