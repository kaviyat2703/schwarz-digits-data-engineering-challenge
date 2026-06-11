
## Q0 - Unified Dataset Creation
Approach:
- Standardized store schemas.
- Extracted country information from stores_v2.
- Merged both versions.
- Resolved overlaps by retaining the latest store version using a window function ordered by version in descending order.

Result:
Produced a unified store dimension suitable for downstream analysis.

## Q1 - Determine how many different stores each product is being sold in
Approach:
- Use the unified store dataset to ensure only valid Lidl Plus stores are considered.
- Join transaction data with the unified store dataset using store_id.
- Group transactions by product.
- Count the number of distinct stores associated with each product.

Result:
product_id, store_count

## Q2 - Identify the store with the second-highest quantity sold for each product
Approach:
- Aggregate transaction quantities at the product and store level.
- Calculate the total quantity sold for each product-store combination.
- Dense ranking is used so that stores with the same sales quantity receive the same rank and all qualifying second-ranked stores are retained.
- Products sold in fewer than two stores will not have a qualifying second store.

Result:
product_id, store_id, total_quantity

## Q3 - Provide a category-level view of the stores identified in Question 2 for marketing campaign planning
Approach:
Reuse the second-highest-selling stores identified in Question 2.
Join the result with product metadata.
Expand category assignments using category explosion so that products belonging to multiple categories contribute to each applicable category.
Group records by category name.
Store collections are deduplicated at category level.
Collect the associated stores into a single list for each category.


Result:
category_name, stores

## Q3 - Considering this ETL complete, we need to productize it. Walk us through the steps you would take to

Detailed version control, deployment, testing, monitoring and operational considerations are documented in docs/productionization.md.