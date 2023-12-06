import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
import datetime

spark = SparkSession \
          .builder \
          .config("spark.master", "local") \
          .appName("interfacing spark sql to hive metastore with no configuration file") \
          .config("hive.metastore.uris", "thrift://10.0.2.15:9083") \
          .enableHiveSupport() \
          .getOrCreate()

sc=spark.sparkContext

sc.setLogLevel("ERROR")

spark.sql("CREATE TABLE IF NOT EXISTS tweets_python (datetime STRING, text STRING) USING hive")

#Set Twitter credential

# Replace the values below with yours
CONSUMER_KEY = '<your consumer key>'
CONSUMER_SECRET = 'Your consumer Secret'
ACCESS_TOKEN = 'Your Access Token'
ACCESS_SECRET = 'Your Access Token Secret'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, time, sys

import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

class MyListener(StreamListener):
    def __init__(self, api=None):
        super().__init__()

    def on_status(self, status):
        
        text = status.text
        created = str(status.created_at)
        record = {'Text': text, 'Created At': created}
#Save to HIVE table tweets        
        filtered_data="".join(list(filter(lambda x: x!="@" and x!="'" and x!='"' \
                                          and x!="\n" and x!='{' and x!='}' and x!='(' and x!=')',text)))
        print(filtered_data)
        spark.sql("INSERT INTO tweets values ('"+created+"','"+filtered_data+"')")


    def on_error(self, status):
        print ('Something wrong with status', status)

    def on_limit(self, status):
        print ('Over the threshold', status)

    def on_timeout(self, status):
        print ('Timeout...')


stream = Stream(auth=auth, listener=MyListener())
stream.filter(track=['stock market'])

'''
Run it:
Ciena CIEN Outpaces Stock Market Gains: What You Should Know 
https://t.co/XFAL2xutM8

RT AnnaApp91838450: BREAKING: Stock Market Soars After Trump Speech To The Nation 
https://t.co/0F9KOlHiesEat
 Your Heart Out CorruptDemoc…
Veeva Systems VEEV Outpaces Stock Market Gains: What You Should Know 
https://t.co/871ROpHNpT

RandyHedgehog Dolan__Ryan CaptainCons We are at Peace. Look at the stock market reaction. No casualties and we… 
https://t.co/JEfDOxkHI4

Innoviva INVA Outpaces Stock Market Gains: What You Should Know 
https://t.co/EIN4xgGC0y

Lrihendry ROHLL5 PRESIDENT TRUMP has been in OFFICE for 3 years and these five things are true. Lowest Unemploym… 
https://t.co/ht8cAE7Ifp
 …



'''
