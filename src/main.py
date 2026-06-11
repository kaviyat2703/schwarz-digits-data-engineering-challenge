from pyspark.sql import SparkSession
from schemas import stores_schema, stores_v2_schema, ticketline_schema, products_schema
from transformations import (
    build_unified_stores,
    calculate_store_counts,
    calculate_second_stores,
    calculate_category_stores,
)
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    spark = SparkSession.builder.appName("schwarz-lidl-plus-DE-challenge").getOrCreate()

    logging.info("Starting pipeline")
    logging.info("Reading source files")

    stores_df = (
        spark.read.schema(stores_schema)
        .option("header", True)
        .csv(str(DATA_DIR / "stores.csv"))
    )

    stores_v2_df = (
        spark.read.schema(stores_v2_schema)
        .option("header", True)
        .csv(str(DATA_DIR / "stores_v2.csv"))
    )

    ticketline_df = (
        spark.read.schema(ticketline_schema)
        .option("header", True)
        .csv(str(DATA_DIR / "ticket_line.csv"))
    )

    products_df = spark.read.schema(products_schema).json(
        str(DATA_DIR / "products.json")
    )

    logging.info("Building unified stores dataset")

    unified_store_df = build_unified_stores(stores_df, stores_v2_df)

    logging.info("Calculating store counts")

    store_counts_df = calculate_store_counts(ticketline_df, unified_store_df).orderBy(
        "product_id"
    )

    logging.info("Calculating second-ranked stores")

    second_stores_df = calculate_second_stores(ticketline_df, unified_store_df).orderBy(
        "product_id", "store_id"
    )
    logging.info("Calculating category stores")

    category_stores_df = calculate_category_stores(
        second_stores_df, products_df
    ).orderBy("category_name")

    logging.info("Writing output datasets")

    store_counts_df.show(truncate=False)
    second_stores_df.show(truncate=False)
    category_stores_df.show(truncate=False)
    # store_counts_df.write.mode("overwrite").csv(
    #     str(OUTPUT_DIR / "store_counts")
    # )

    # second_stores_df.write.mode("overwrite").csv(
    #     str(OUTPUT_DIR / "second_stores")
    # )

    # category_stores_df.write.mode("overwrite").csv(
    #     str(OUTPUT_DIR / "category_stores")
    # )

    logging.info("Pipeline completed successfully")

    spark.stop()


if __name__ == "__main__":
    main()
