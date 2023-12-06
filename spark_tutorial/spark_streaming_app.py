from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Function to print each tweet in an RDD
def process_rdd(rdd):
    try:
        # Collect the RDD to a list
        tweets = rdd.collect()
        # Print each tweet in the list
        for tweet in tweets:
            print(tweet)
    except:
        pass

# Spark context setup
sc = SparkContext(appName="PythonStreamingTwitter")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 1)  # 1 second window

# Define the socket where the tweets will be received
TCP_IP = "localhost"
TCP_PORT = 9009

# Create a DStream that represents streaming data from a TCP source
lines = ssc.socketTextStream(TCP_IP, TCP_PORT)

# Process each RDD in each time interval
lines.foreachRDD(process_rdd)

# Start the streaming process
ssc.start()
ssc.awaitTermination()
