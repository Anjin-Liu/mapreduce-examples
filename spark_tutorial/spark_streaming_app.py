from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def process_rdd(rdd):
    # Check if RDD is empty
    if not rdd.isEmpty():
        # Collect items in RDD
        collected_data = rdd.collect()
        for number in collected_data:
            print(f"Received number: {number}")

sc = SparkContext("local[2]", "NumberStreamApp")
ssc = StreamingContext(sc, 1)

TCP_IP = 'localhost'
TCP_PORT = 9010

# Create a DStream that represents streaming data from a TCP source
lines = ssc.socketTextStream(TCP_IP, TCP_PORT)

# Process each RDD in each time interval
lines.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
