
class OutputSink:
    @staticmethod
    def write_to_console(result_df):
        return result_df.writeStream.format("console").outputMode("append").start()

    @staticmethod
    def write_to_file(result_df):
        return (result_df
                .writeStream
                .format("csv")
                .option("path", "../dataset/crime_data/output/")
                .option("checkpointLocation", "../dataset/crime_data/checkpoint_dir/")
                .outputMode("append")
                ).start()
