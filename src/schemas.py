from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    IntegerType,
    ArrayType
)

stores_schema = StructType([
    StructField("store_id", LongType(), False),
    StructField("country", StringType(), True),
    StructField("version", StringType(), True)
])

stores_v2_schema = StructType([
    StructField("store_id", StringType(), False),
    StructField("version", StringType(), True)
])

ticketline_schema = StructType([
    StructField("ticket_id", LongType(), False),
    StructField("product_id", LongType(), False),
    StructField("store_id", LongType(), False),
    StructField("date", StringType(), True),
    StructField("quantity", IntegerType(), True)
])

category_schema = StructType([
    StructField("category_id", LongType(), True),
    StructField("category_name", StringType(), True)
])

products_schema = StructType([
    StructField("product_id", LongType(), False),
    StructField("product_name", StringType(), True),
    StructField("categories", ArrayType(category_schema), True)
])