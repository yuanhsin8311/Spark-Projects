sc

# Set up the file paths for data 
# If it's on the local system append file:// to the beginning of the path 
# If it's on hdfs append hdfs://

airlinePath = "hdfs:///user/yuanhsin/flightDelaysData/airlines.csv"
airportPath = "hdfs:///user/yuanhsin/flightDelaysData/airports.csv"
flightPath = "hdfs:///user/yuanhsin/flightDelaysData/flights.csv"

# Use SparkContext initialized by pyspark to load the data
# sc: SparkContext variable ie. the connection to spark
# textFile: tell sparkContext to load data from a text file into memory
airlines=sc.textFile(airlinesPath)

# Airlines is an RDD 
print airlines

# View the full dataset 
airlines.collect()
# Get the first line
airlines.first()
# Get the first 10 lines 
airlines.take(10)
# Count 
airlines.count()

## Transformation and Actions: filter-> transformation -> (1)filter the header (2)split by comma (3)convert alrline code to integer
                               take -> action
# Filter the header "Description" out 
# Filter function takes a boolean function
# The filter returns another RDD
airlinesWoHeader = airlines.filter(lambda x:"Description" not in x)
print airlinesWoHeader
airlinesWoHeader.take(10)

# RDD knows their lineage; RDD holds the metadata
# Data is processed only when the users request a result(take actions) 
# lazy evaluation ->fast computation
# spark will keep a record of the series of transformations requested by the user -> efficiently group the transformation and execute 
airlinesParsed=airlinesWoHeader.map(lambda x:x.split(",")).take(10)
print airlinesParsed
# map(function)
airlines.map(len).take(10)    

def notHeader(row):
    return "Description" not in row
airlines.filter(notHeader).take(10)

# Chain transformations together 
airlines.filter(notHeader).map(lambda x: x.split(',')).take(10)

# Use Python libraries 
import csv 
from StringIO import StringIO

def split(line):
    reader = csv.reader(StringIO(line))
    return reader.next()

airlines.filter(notHeader).map(split).take(10)




























