import os

os.environ["PYSPARK_PYTHON"] = (
    r"C:\Users\KAVIYA\AppData\Local\Programs\Python\Python310\python.exe"
)
os.environ["PYSPARK_DRIVER_PYTHON"] = (
    r"C:\Users\KAVIYA\AppData\Local\Programs\Python\Python310\python.exe"
)


from pyspark.sql import SparkSession

from src.transformations import (
    build_unified_stores,
    calculate_store_counts,
    calculate_second_stores,
    calculate_category_stores,
)

spark = (
    SparkSession.builder.master("local[1]")
    .appName("unit-tests")
    .config(
        "spark.pyspark.python",
        r"C:\Users\KAVIYA\AppData\Local\Programs\Python\Python310\python.exe",
    )
    .config(
        "spark.pyspark.driver.python",
        r"C:\Users\KAVIYA\AppData\Local\Programs\Python\Python310\python.exe",
    )
    .getOrCreate()
)


def test_build_unified_stores():
    stores_data = [(45, "DE", "1")]
    stores_v2_data = [("DE45", "2")]
    stores_df = spark.createDataFrame(stores_data, ["store_id", "country", "version"])

    stores_v2_df = spark.createDataFrame(stores_v2_data, ["store_id", "version"])

    result_df = build_unified_stores(stores_df, stores_v2_df)

    result = result_df.collect()

    assert result_df.count() == 1

    assert result[0]["version"] == 2


def test_calculate_store_counts():
    ticketline_data = [(1, 45), (1, 45), (1, 46)]
    unified_store_data = [(45,), (46,)]

    ticketline_df = spark.createDataFrame(ticketline_data, ["product_id", "store_id"])

    unified_store_df = spark.createDataFrame(unified_store_data, ["store_id"])

    result_df = calculate_store_counts(ticketline_df, unified_store_df)

    result = result_df.collect()

    assert result[0]["product_id"] == 1


def test_calculate_second_stores():
    ticketline_data = [(1, 45, 100), (1, 46, 80), (1, 47, 80), (1, 48, 50)]

    unified_store_data = [(45,), (46,), (47,), (48,)]

    ticketline_df = spark.createDataFrame(
        ticketline_data, ["product_id", "store_id", "quantity"]
    )

    unified_store_df = spark.createDataFrame(unified_store_data, ["store_id"])

    result_df = calculate_second_stores(ticketline_df, unified_store_df)

    result = result_df.collect()

    stores = [row["store_id"] for row in result]

    assert result_df.count() == 2
    assert set(stores) == {46, 47}


def test_calculate_category_stores():

    second_stores_data = [(6, 40), (7, 40), (7, 41)]

    products_data = [
        (6, [{"category_id": 1026, "category_name": "Cookies"}]),
        (
            7,
            [
                {"category_id": 1026, "category_name": "Cookies"},
                {"category_id": 1025, "category_name": "Cereal"},
            ],
        ),
    ]

    second_stores_df = spark.createDataFrame(
        second_stores_data, ["product_id", "store_id"]
    )

    products_df = spark.createDataFrame(products_data, ["product_id", "categories"])

    result_df = calculate_category_stores(second_stores_df, products_df)

    result = result_df.collect()

    result_dict = {row["category_name"]: set(row["stores"]) for row in result}

    assert result_dict["Cookies"] == {40, 41}
    assert result_dict["Cereal"] == {40, 41}
