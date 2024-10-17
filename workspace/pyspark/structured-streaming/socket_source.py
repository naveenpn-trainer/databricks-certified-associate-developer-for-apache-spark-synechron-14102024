from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode

if __name__ == '__main__':
    spark = (SparkSession
             .builder
             .appName("Streaming Demo")
             .master("local")
             .config("spark.sql.shuffle.partitions", 10)
             .config("spark.jars", "../lib/mysql-connector-java-8.0.28.jar").getOrCreate())

    # inputDF = spark.readStream.format("socket").option("host","localhost").option("port","9999").load()
    inputDF = spark.readStream.load(format="socket",
                                    host="localhost",
                                    port="9999")
    print(inputDF.isStreaming)
    jdbc_url = "jdbc:mysql://localhost:3306/streaming_db"
    jdbc_properties = {
        "user": "root",
        "password": "qwerty",
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    # result_df = inputDF.select(explode(split(col("value"),",")).alias("words")).groupBy("words").count()
    inputDF.writeStream.outputMode("update").foreachBatch(
        lambda df, id: df.write.jdbc(jdbc_url, "demo_tbl", mode="append",
                                     properties=jdbc_properties)).start().awaitTermination()
