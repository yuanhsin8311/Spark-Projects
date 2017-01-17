# Marvel Social Network

from graphframes import *

edgesPath = "hdfs:///user/yuanhsin/spark/Marvel/Edges.csv"
verticesPath = "hdfs:///user/yuanhsin/spark/Marvel/Vertices.csv"

# Use SQLConext to set up the DataFrames
from pyspark.sql import SQLContext,Row
sqlC = SQLContext(sc)

edges = sqlC.createDataFrame(sc.textFile(edgesPath)).map(lambda x: x.split(",")).
edges=sqlC.createDataFrame\
    (sc.textFile(edgesPath)\
    .map(lambda x:x.split(","))\
    .map(lambda x:[int(y) for y in x])\
    ,["src","dst","wt"])
    
vertices=sqlC.createDataFrame\
    (sc.textFile(verticesPath)\
    .map(lambda x:x.split("|"))\
    .map(lambda x:[int(x[0]),x[1],x[2]])\
    ,["id","name","wt"])
marvelSocial=GraphFrame(vertices, edges)
degrees=marvelSocial.degrees
degrees
degrees.take(10)
