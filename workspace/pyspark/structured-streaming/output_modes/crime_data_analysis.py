from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
from pyspark.sql.types import *


def write_batch_to_db(batch_df, batch_id):
    jdbc_url = "jdbc:mysql://localhost:3306/streaming_db"
    jdbc_properties = {
        "user": "root",
        "password": "qwerty",
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    batch_df.write.jdbc(jdbc_url, "crime_statistics", mode="overwrite",
                        properties=jdbc_properties)


def write_stream_to_db(result_df):
    return (result_df
    .writeStream
    .outputMode("complete")
    .foreachBatch(
        lambda batch_df, batch_id: write_batch_to_db(batch_df, write_batch_to_db))).start().awaitTermination()


if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("Streaming Demo")
             .master("local")
             .config("spark.sql.shuffle.partitions", 10)
             .config("spark.jars", "../../lib/mysql-connector-java-8.0.28.jar")
             .getOrCreate())

    CRIME_SCHEMA = StructType([
        StructField("code", StringType()),
        StructField("borough", StringType()),
        StructField("major_category", StringType()),
        StructField("minor_category", StringType()),
        StructField("value", IntegerType()),
        StructField("year", IntegerType()),
        StructField("month", IntegerType())
    ])

    input_df = spark.readStream.load(path="../../dataset/crime_data/source/", format="csv", schema=CRIME_SCHEMA)

    # Incremental Query
    result_df = input_df.groupBy("borough").agg(sum("value").alias("total_value"))
    # result_df.writeStream.format("console").outputMode("update").start().awaitTermination()
    write_stream_to_db(result_df)