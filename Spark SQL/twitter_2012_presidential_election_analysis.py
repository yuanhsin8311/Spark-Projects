# Dataset (JSON file):
# https://datahub.io/dataset/twitter-2012-presidential-election/resource/9bb14d78-9519-459a-9fad-e630e3e9a0a1?inner_span=True

# hdfs cli:
# fileZilla: upload data to server's folder /spark
# ls /spark/
# hdfs dfs -mkdir -p /user/yuanhsin/spark/sparkSQL
# hdfs dfs -ls -R /user/yuanhsin/spark
# hdfs dfs -moveFromLocal  spark/cache-0-json  /user/yuanhsin/spark/sparkSQL/

# Spark SQL:

twitterPath = "hdfs:///user/yuanhsin/spark/sparkSQL/cache-0-json"

## Use Python's JSON parser to parse the data 
import json
twitterData = sc.textFile(twitterPath).map(lambda x: json.loads(x))  # twitterData is an RDD where each record is a dictionary
twitterData.take(10)  # Each record has all details of a single tweet

# select text from twitterData where screen_name = "realDonaldTrump" limit 10;
twitterData.filter(lambda x: x['user']['screen_name'] == "realDonaldTrump").map(lambda x: x['text']).take(10)

# Load data into RDDs using a sparkContext
# Load data into a DataFrame using sqlContext 
from pyspark.sql import SQLContext, Row 
sqlC=SQLContext(sc)    # Use the sparkContext to set up the sqlContext
twitterTable = sqlC.read.json(twitterPath)  # In-memory database

# Before using SparkSQL, to register the table's name to the SQLContext is necessary 
twitterTable.registerTempTable("twitterTable")    # "twitterTable" DataFrame's alias
sqlC.sql("select text, user.screen_name from " +\ 
         "twitterTable where user.screen_name = 'realDonaldTrump' +\
         "limit 10").collect()
# DataFrame are made up of ROW objects
# Row objects are like structs

twitterTable.take(10)
twitterTable.map(lambda x:x.text).take(10)
