from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    substring,
    row_number,
    countDistinct,
    sum,
    dense_rank,
    explode,
    collect_set,
)
from pyspark.sql.window import Window


# Standardize store schemas and retain latest version.
def build_unified_stores(stores_df: DataFrame, stores_v2_df: DataFrame) -> DataFrame:
    stores_v1_standardized = stores_df.withColumn("version", col("version").cast("int"))
    stores_v2_standardized = (
        stores_v2_df.withColumn("country", substring(col("store_id"), 1, 2))
        .withColumn("store_id", substring(col("store_id"), 3, 10).cast("long"))
        .withColumn("version", col("version").cast("int"))
    )

    stores_v1_standardized = stores_v1_standardized.select(
        "store_id", "country", "version"
    )
    stores_v2_standardized = stores_v2_standardized.select(
        "store_id", "country", "version"
    )
    stores_unified = stores_v1_standardized.unionByName(stores_v2_standardized)

    window_spec = Window.partitionBy("store_id", "country").orderBy(
        col("version").desc()
    )
    ranked_store = stores_unified.withColumn("rnk", row_number().over(window_spec))
    unified_store_df = ranked_store.filter(col("rnk") == 1).drop("rnk")

    return unified_store_df


# identify different stores where each product is being sold in
def calculate_store_counts(
    ticketline_df: DataFrame, unified_store_df: DataFrame
) -> DataFrame:
    joined_df = ticketline_df.join(unified_store_df, ["store_id"], "inner")
    store_counts_df = joined_df.groupBy("product_id").agg(
        countDistinct("store_id").alias("store_count")
    )

    return store_counts_df


# identify second best performing store per product based on quantity sold.
def calculate_second_stores(
    ticketline_df: DataFrame, unified_store_df: DataFrame
) -> DataFrame:
    joined_df = ticketline_df.join(unified_store_df, ["store_id"], "inner")
    sales_by_store_df = joined_df.groupBy("store_id", "product_id").agg(
        sum("quantity").alias("total_sum")
    )

    window_spec = Window.partitionBy("product_id").orderBy(col("total_sum").desc())
    ranked_stores = sales_by_store_df.withColumn("rnk", dense_rank().over(window_spec))
    second_stores_df = (
        ranked_stores.filter(col("rnk") == 2)
        .drop("rnk")
        .select("product_id", "store_id", "total_sum")
    )

    return second_stores_df


# Identify product category for the list of second_stores for advertising campaign
def calculate_category_stores(
    second_stores_df: DataFrame, products_df: DataFrame
) -> DataFrame:

    joined_df = second_stores_df.join(products_df, "product_id", "inner")
    explode_df = joined_df.withColumn("category", explode("categories"))

    category_stores_df = (
        explode_df.withColumn("category_name", col("category.category_name"))
        .groupBy("category_name")
        .agg(collect_set("store_id").alias("stores"))
    ).select("category_name", "stores")

    return category_stores_df
