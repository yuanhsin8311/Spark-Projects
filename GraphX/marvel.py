# Marvel Social Network

from graphframes import *

edgesPath = "hdfs:///user/yuanhsin/spark/Marvel/Edges.csv"
verticesPath = "hdfs:///user/yuanhsin/spark/Marvel/Vertices.csv"

# Use SQLConext to set up the DataFrames
from pyspark.sql import SQLContext,Row
sqlC = SQLContext(sc)

# The read method is used when reading data from files
# createDataFrame(RDD,schema)
# RDD: load the data from file into an RDD, parse the rows and give it to createDataFrame()
# schema: explicitly specify the schema when using createDataFrame()
edges = sqlC.createDataFrame(sc.textFile(edgesPath))\
        .map(lambda x: x.split(","))\
        .map(lambda x: [int(y) for y in x])\
        ,["src","dst","wt"])    # edge weight: the count of the number of times the 2 characters appear together
        
vertices = sqlC.createDataFrame(sc.textFile(verticesPath)
           .map(lambda x: x.split("|"))\
           .map(lambda x: [int(x[0]),x[1],x[2]])\
           ,["id","name","wt"])
# Create a DataFrame
from graphframes import *
marvelSocial = GraphFrame(vertices,edges)

# The degrees attribute will tell the number of connections a vertex has
# find most important(well-connected) characters
# Degrees is another dataframe
degrees=marvelSocial.degrees
degrees
degrees.take(10)

# sort top 10 columns by degrees
from pyspark.sql.functions import col
top10 = degress.sort(col("degree").desc()).take(10)

# Print out the character names for the ids
for character in top10:     # each member of top10 list is a ROW object
        charid = character.id
        print vertices.filter("id="+str(charid)).first().name
        # filter transformation for dataframe is slightly different; use a string as the condition instead of lambda function

        
        
        
        
        
