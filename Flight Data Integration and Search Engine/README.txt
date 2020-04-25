#There are two files: 
#1.Python file to clean the data and for the visualization.
#2.Bash file for search engine using AsterixDB and MongoDB.

#Data Cleaning has been done on the cluster and can be run using spark-submit:
$spark-submit cleaning_visualization.py

#The search engine cannot be done on the cluster as there is no permission to install mongoDB and install AsterixDb on the cluster(It can be done locally).
#To run the search engine:
$./search.sh

#The visualization part cannot be performed on the cluster as following libraries are not available:
#matplotlob, seaborn, sklearn, basemap(mpl_toolkits.basemap), scipy