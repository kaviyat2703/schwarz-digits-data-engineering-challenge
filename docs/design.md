## Problem Understanding

The challenge consists of:

- Schema unification across store datasets
- Product sales aggregations
- Ranking logic
- Category-level aggregations
- Production readiness considerations

The pipeline follows a  batch ETL flow:Ingest → Transform → Analyze →  <NOTE>


## Data Model

Products
Stores V1
Stores V2
TicketLines

## Store Unification Approach

The challenge contains two versions of store reference data with different schemas.To create a consistent store dimension for downstream analysis:

- Both datasets are standardized into a common structure consisting of:

    store_id      BIGINT
    country       STRING
    version       INT

- For records from the newer schema version, country information is extracted from the store_id prefix and the numeric store identifier is    standardized to match the legacy schema. <NOTE>

- The datasets are combined into a single unified store dataset.

- Where the same store exists in multiple versions, the most recent version is retained.

- A window function using row_number() ordered by version in descending order is used to retain the latest version of each store.

This approach ensures compatibility with TicketLines data as it references store_id as integer so keeping numeric store_id in unified dataset makes joins easier while retaining country information.

## Ranking Logic

- Store performance is calculated using the total quantity sold per product and store combination.

- A window function using dense_rank() is applied within each product to rank stores by quantity sold.

- Dense ranking was selected to ensure that stores with equal sales quantities receive the same rank. This allows all qualifying second-ranked stores to be retained rather than selecting one store arbitrarily.



## Architecture / Code Organization
The solution is organized into separate modules:

- schemas.py: Explicit Spark schemas for all source datasets.
- transformations.py: Reusable business transformations.
- main.py: Pipeline orchestration, input reading and output writing.
- tests/: Unit tests for key transformation logic.


This separation improves maintainability, readability and testability.

Business logic is isolated from orchestration, allowing transformations to be tested independently from file ingestion and output generation.

## Schema Design

Explicit Spark schemas are used instead of schema inference.

Benefits:

- Consistent data types
- Faster file reads
- Reduced risk of incorrect type inference
- Clear documentation of expected input structure


## Category Aggregation Logic

- Products may belong to multiple categories.

- The categories array is exploded into individual category records before aggregation.

- Stores are collected using collect_set() to return unique stores per category.

## Testing Approach

Unit tests are provided for business transformations including:

- Store unification
- Store count calculation
- Second-ranked store identification
- Category-level store aggregation

The tests validate business rules independently of file I/O and pipeline execution.


## Idempotency

 The pipeline uses overwrite semantics when writing outputs. This ensures idempotent execution, allowing the same batch to be safely reprocessed without producing duplicate results.

 Given the same input datasets, the transformations are deterministic and will produce the same outputs on every execution.

