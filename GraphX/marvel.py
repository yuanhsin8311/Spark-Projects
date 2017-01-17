# Marvel Social Network:
# (1)Vertices: characters
#    - Size of vertice is proportional to the number of times the character appears in any comic book
# (2)Edges: a relationship between two characters
#    - Edge weight is proportional to the number of times the characters appear together
     - co-occurence network
from graphframes import *
edgesPath="hdfs:///user/swethakolalapudi/Marvel/Edges.csv"
verticesPath="hdfs:///user/swethakolalapudi/Marvel/Vertices.csv"
