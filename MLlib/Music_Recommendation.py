# Audioscrobbler is an online music recommendation service
# Dataset:  http://www-etud.iro.umontreal.ca/~bergstrj/audioscrobbler_data.html

# Use FillZilla to upload data to server
# hdfs cli:
ls spark
hdfs dfs -mkdir -p /user/yuanhsin/spark/audio/
hdfs dfs -copyFromLocal spark/user_artist_data.txt  /user/yuanhsin/spark/audio/
hdfs dfs -ls -R /user/yuanhsin/

pyspark

rawdataPath ="hdfs:///user/yuanhsin/spark/audio/user_artist_data.txt"

# Loasd the dataset with user-artist ratings
rawUserArtistData = sc.textFile(rawdataPath)
rawUserArtistData.take(10)

# Extract the rating column
rawUserArtistData.map(lambda x: float(x.split(" ")[2])).stats()  # stats() only works for numeric RDDs

# To filter out low ratings if running this algorithm on a local machine will help:
# 1. reduce the amount of processing
# 2. reduce the amount of data held in-memory 
# Rating Objects RDD
from pyspark.mllib.recommendation import Rating,ALS
# Convert a list into a Rating object(User-Product-Rating)
uaData = rawUserArtistData.map(lambda x: x.split(" ")).filter(lambda x: float(x[2]) >= 20).map(lambda x: Rating(x[0],x[1],x[2]))
uaData.persist()    # ALS will pass over this RDD many times 
                    # Persisting will make this computation much faster                                                                     

uaData.take(10)

# ALS has two methods: (1)trainImplicit(data,number of hidden factors it should look for) (2)train
model = ALS.trainImplicit(uaData,10,5,0.01)

user = 1000002
recommendations=model.recommendProducts(user,5)
recommendations
artistsPath="hdfs:///user/swethakolalapudi/audio/artist_data.txt"
artistLookup=sc.textFile(artistsPath).map(lambda x:x.split("\t"))
artistLookup.persist()
userArtists=rawUserArtistData\
    .map(lambda x:x.split(" "))\
    .filter(lambda x:int(x[0])==user and int(x[2])>50)\
    .map(lambda x:x[1]).collect()
for artist in userArtists: 
    print artistLookup.lookup(artist)
    
for rating in recommendations: 
    print artistLookup.lookup(str(rating.product))
