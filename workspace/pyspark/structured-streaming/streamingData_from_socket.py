from pyspark.sql import SparkSession


def create_spark_session():
    return (SparkSession
            .builder
            .appName("Streaming Demo")
            .master("local")
            .config("spark.sql.shuffle.partitions", 10)
            .config("spark.jars", "../lib/mysql-connector-java-8.0.28.jar").getOrCreate())


def read_stream_data(spark):
    return spark.readStream.load(format="socket",
                                 host="localhost",
                                 port="9999")


def write_batch_to_db(batch_df, batch_id):
    jdbc_url = "jdbc:mysql://localhost:3306/streaming_db"
    jdbc_properties = {
        "user": "root",
        "password": "qwerty",
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    batch_df.write.jdbc(jdbc_url, "demo_tbl", mode="append",
                        properties=jdbc_properties)


def write_stream_to_db(result_df):
    return (result_df
            .writeStream
            .outputMode("update")
            .foreachBatch(
        lambda batch_df, batch_id: write_batch_to_db(batch_df, write_batch_to_db))).start().awaitTermination()


def process_stream_data(input_df):
    return input_df


if __name__ == '__main__':
    spark = create_spark_session()
    input_df = read_stream_data(spark)
    result_df = process_stream_data(input_df)
    write_stream_to_db(result_df)
