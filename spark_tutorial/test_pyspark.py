from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PySparkTest") \
    .getOrCreate()
