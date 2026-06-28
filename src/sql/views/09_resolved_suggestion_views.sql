-- A is a sibling of B, B rejected parent C, supress vendor customer A -> parent account C
CREATE OR REPLACE VIEW rejected_effective_vendor_customer_to_parent_map AS (
-- inferred rejections
SELECT
  base.left_vendor_customer_id AS vendor_customer_id,
  rejected.parent_account_id AS parent_account_id,
  'sibling_inferred' AS rejection_type,
  base.right_vendor_customer_id AS source_vendor_customer_id
FROM accepted_normalized_vendor_customer_sibling_map base
JOIN rejected_vendor_customer_to_parent_account_map rejected ON
  base.right_vendor_customer_id = rejected.vendor_customer_id

UNION

-- original rejections
SELECT
  vendor_customer_id,
  parent_account_id,
  'direct_rejection' AS rejection_type,
  NULL AS source_vendor_customer_id
FROM rejected_vendor_customer_to_parent_account_map
);

-- candidate pairs, A is parentless, B has a parent, should A roll up to B's parent?
CREATE OR REPLACE VIEW suggested_parents AS (
WITH filtered AS (
SELECT 
  base.left_vendor_customer_id AS vendor_customer_id,
  right_parent.parent_account_id,
  base.suggestion_type,
  base.priority
FROM vendor_customer_candidate_sibling_map base
JOIN accepted_vendor_customer_to_parent_account_map right_parent ON
  base.right_vendor_customer_id = right_parent.vendor_customer_id

-- exclude inferred and direct rejections
WHERE 
  NOT EXISTS (
    SELECT 1
    FROM rejected_effective_vendor_customer_to_parent_map rejected
    WHERE base.left_vendor_customer_id = rejected.vendor_customer_id
    AND right_parent.parent_account_id = rejected.parent_account_id
  )
  
  -- exclude pairings already confirmed
  AND NOT EXISTS (
    SELECT 1
    FROM accepted_vendor_customer_to_parent_account_map accepted
    WHERE base.left_vendor_customer_id = accepted.vendor_customer_id
  )

), ranked AS (
SELECT 
-- normalize ranking for highest priority available 
  base.*,
  ROW_NUMBER() OVER (
    PARTITION BY base.vendor_customer_id, base.parent_account_id
    ORDER BY priority ASC
  ) AS rn
FROM filtered base
) 
-- filter by highest priority
SELECT 
  vendor_customer_id,
  parent_account_id,
  suggestion_type,
  priority
FROM ranked
WHERE rn = 1
);