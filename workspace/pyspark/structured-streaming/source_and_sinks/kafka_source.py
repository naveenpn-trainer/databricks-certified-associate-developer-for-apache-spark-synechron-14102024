from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("Streaming Demo")
             .master("local")
             .config("spark.sql.shuffle.partitions", 10)
             .config("spark.jars",
                     "../../lib/kafka-clients-2.1.1.jar,../../lib/spark-sql-kafka-0-10_2.12-3.2.1.jar,../../lib/spark-token-provider-kafka-0-10_2.12-3.4.1.jar,../../lib/commons-pool2-2.11.1.jar")
             .getOrCreate())

    input_df = (spark
                .readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "my-demo-topic")
                .load())

    # input_df.printSchema()
    result_df = input_df.select(col("value").cast(StringType()))
    result_df.writeStream.format("console").option("truncate", "false").outputMode("update").start().awaitTermination()
