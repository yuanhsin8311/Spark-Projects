# Objective: monitor all text data that arrives at a certain port and filter any lines that contain the word "error",
#            print a count to screen

import sys

# Set up the SparkContext and StreamingContext
# StreamingContext is used to create DStreams
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


if __name__ == "__main__":

    sc = SparkContext(appName="StreamingErrorCount")
    ssc = StreamingContext(sc, 1)    # 1 is batch interval(1 second) for all DStreams
    
    # Fault-Tolerance: set a specified location where a backup of the data is saved at a certain frequency
    ssc.checkpoint("hdfs:///user/yuanhsin/streaming") 
    
    # Build DStreams
    # sys.argv[1]: hostname where the data will arrive 
    # int(sys.argv[2]): port where the data arrives
    # Both these arguments will be passed at the command line when submitting this script
    # >spark-submit Streaming.py localhost 9999
    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    
    counts = lines.flatMap(lambda line: line.split(" "))\
                  .filter(lambda word:"ERROR" in word)\
                  .map(lambda word: (word, 1))\
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()
    
    
    sc = SparkContext(appName="StreamingErrorCount")
    ssc = StreamingContext(sc,1)
    ssc.checkpoint("hdfs:///user/yuanhsin/streaming")
    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    counts = lines.flatMap()
