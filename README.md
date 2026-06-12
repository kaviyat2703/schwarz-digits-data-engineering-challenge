
## Project Overview

This solution processes daily batch data using PySpark.

The pipeline:

1. Standardizes and merges store datasets
2. Identifies the number of different stores selling each product
3. Identifies second-best-performing stores per product based on quantity sold
4. Groups second-best-performing stores by product category

The implementation focuses on modularity, testability, clear schemas and production-grade design

## Project Structure

data/
docs/
output/
src/
tests/
README.md
requirements.txt

## Running the Pipeline

## Running the Pipeline

pip install -r requirements.txt

From the project root:

python src/main.py

## Running Tests

python -m pytest tests

## Outputs
output/
  store_counts
  second_stores
  category_stores

## Assumptions
- Only stores present in the unified store dataset are considered in downstream calculations.
- When a store exists in multiple schema versions, the latest version is retained.
- Store performance is determined by total quantity sold per product.
- Products may belong to multiple categories and are associated with each applicable category.
- Category names are assumed to be unique within the provided dataset and are used for grouping to align with the business requirement.

## Design Decisions
- Explicit Spark schemas are used to avoid schema inference and improve data consistency.
- Store datasets are standardized into a common schema before analysis.
- Window functions are used to retain the latest store version and identify second-ranked stores.
- Business logic is implemented as reusable transformation functions to improve modularity and testability.
- Unit tests are provided for all core transformation functions using small in-memory Spark DataFrames.

Detailed assumptions, design considerations and productionization notes are documented under the docs/ directory.

docs/assumptions.md
docs/design.md
docs/productionization.md
