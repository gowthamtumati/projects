There are two datasets for this. One with information about weather stations and other is a collection of records for 4 years.

In this project, we find out the stable rainfall in all the states in the US.

For this, we create a local instance of spark and carry out the operations.

To run :
$ spark-submit weather.py [locations_path] [recordings_path] [output_path]