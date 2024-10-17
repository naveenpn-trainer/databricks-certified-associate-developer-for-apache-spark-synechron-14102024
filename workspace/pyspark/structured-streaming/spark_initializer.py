from pyspark.sql import SparkSession


class SparkInitializer:
    @staticmethod
    def get_spark_session():
        return (SparkSession
         .builder
         .appName("Streaming Demo")
         .master("local")
         .config("spark.sql.shuffle.partitions", 10)
         .config("spark.jars", "../lib/mysql-connector-java-8.0.28.jar").getOrCreate())