#File to execute the following modules of the Part-A of the program.

# $1=indexed data directory; $2=crawled data directory; $3=Number of tweets to be crawled

#Crawler:

python crawler.py $2 $3

#Indexer:
java -jar tse-0.0.1-SNAPSHOT-jar-with-dependencies.jar $1 $2 1

#Search Engine:
java -jar tse-0.0.1-SNAPSHOT-jar-with-dependencies.jar $1 2

