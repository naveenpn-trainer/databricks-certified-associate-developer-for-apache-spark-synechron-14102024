
from pyspark.sql.functions import col
from pyspark.sql.types import *
from spark_initializer import SparkSession
from output_sink import OutputSink



if __name__ == '__main__':
    spark = SparkSession.get_spark_session()

    CRIME_SCHEMA = StructType([
        StructField("code", StringType()),
        StructField("borough", StringType()),
        StructField("major_category", StringType()),
        StructField("minor_category", StringType()),
        StructField("value", IntegerType()),
        StructField("year", IntegerType()),
        StructField("month", IntegerType())
    ])

    inputDF = spark.readStream.load(path="../dataset/crime_data/source/", format="csv", schema=CRIME_SCHEMA)

    # Incremental Query
    resultDF = inputDF.filter(col("year") == 2012)

    consoleStreamingQuery = OutputSink.write_to_console(resultDF)
    fileStreamingQuery = OutputSink.write_to_file(resultDF)
    consoleStreamingQuery.awaitTermination()
    fileStreamingQuery.awaitTermination()
