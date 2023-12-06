from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json

def process_rdd(rdd):
    for record in rdd.collect():
        print(record)

sc = SparkContext("local[2]", "RedditStreamApp")
ssc = StreamingContext(sc, 1)

TCP_IP = 'localhost'
TCP_PORT = 9010

lines = ssc.socketTextStream(TCP_IP, TCP_PORT)
lines.foreachRDD(lambda rdd: rdd.foreach(process_rdd))

ssc.start()
ssc.awaitTermination()
