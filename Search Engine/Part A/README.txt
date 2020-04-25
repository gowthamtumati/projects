# The directory contains following files:
# Code files, jar file, bash file, Mid-term Report
 
# Dependancies:
# Python 2 should be installed and working on the system where crawler is being exected.

#To execute the entire part A of the project:
$ bash execute_partA.sh <index-file-directory> <crawled-data-directory> <number-of-tweets-to-crawl>
#eg bash execute_partA.sh /Users/lavidhaliwal/Desktop/cs242/indexed/ /Users/lavidhaliwal/Desktop/cs242/crawled/ 1000


#To execute the files separately, perform following actions:

# 1. To execute the crawler, run the following command:

$ python <file-name> <crawled-data-directory> <number-of-tweets-to-crawl>
#eg: python tweets_crawl.py /Users/lavidhaliwal/Desktop/cs242/crawled/ 1000


# 2. To execute the indexer, run the following command:

$ java -jar <jar-file> <index-file-directory> <crawled-data-directory> 1
#eg: java -jar tse-0.0.1-SNAPSHOT-jar-with-dependencies.jar /Users/lavidhaliwal/Desktop/cs242/indexed/ /Users/lavidhaliwal/Desktop/cs242/crawled/ 1


# 3. To execute the search engine, run the following command: 

$ java -jar <jar-file> <index-file-directory> 2
#eg: java -jar tse-0.0.1-SNAPSHOT-jar-with-dependencies.jar /Users/lavidhaliwal/Desktop/cs242/indexed/ 2
