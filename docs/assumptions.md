## Assumption 1 ##

Only stores present in the unified store dataset are considered in downstream calculations.

Reason:
The challenge states that not all stores participate in the Lidl Plus program.Joining with the unified store dataset ensures that only participating Lidl Plus stores are included in the analysis.

## Assumption 2 ##

When multiple records exist for the same store, the record with the highest version number is considered the latest and is retained.

Reason:
The version field is assumed to represent the target store metadata over time. Retaining the highest version ensures downstream analysis uses the most recent store definition available.

## Assumption 3 ##

Store performance is determined by the total quantity sold for a given product across all transactions.
When multiple stores qualify for the second position due to equal sales quantities, all qualifying stores are retained.

Reason: The requirement explicitly refers to total quantity sold and Stores with equivalent performance should be treated equally rather than selecting one randomly.

## Assumption 4 ##

Products may belong to multiple categories. When this occurs, the corresponding store is associated with each applicable category.

Reason:
The source product data contains products assigned to more than one category.


## Assumption 5 ##

Store collections are deduplicated at category level.

If the same store is associated with multiple products within a category, it is returned only once.

Reason : Marketing is interested in the list of stores per category rather than repeated occurrences of the same store.
