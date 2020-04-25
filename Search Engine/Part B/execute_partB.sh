#To execute the InvertedIndexGenerator:
hdfs dfs -mkdir /CS242_Grp13 
hdfs dfs -mkdir /CS242_Grp13/Input
hdfs dfs -put tweets_data0.txt /CS242_Grp13/Input  
hadoop jar abc.jar InvertedIndexGenerator Input/tweets_data0.txt /Output
#If this doesn't work; 2 jar files need to be added. To do this, I have provided the jars in the zip called jars.zip.	

