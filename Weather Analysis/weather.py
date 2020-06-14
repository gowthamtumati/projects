
import timeit
import sys

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import substring
from datetime import datetime

from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

locations = sys.argv[1]
recording = sys.argv[2]
output_loc = sys.argv[3]


#Code block for Task 1
start = timeit.default_timer()

sprkctxt = SparkContext('local')
sqlcontext = SQLContext(sprkctxt)

spark = SparkSession(sprkctxt)
data_locations = spark.read.option("header", "true").csv(locations)
grouped_data_locations = data_locations.filter(data_locations["CTRY"] == "US").groupBy("STATE")

#Code block for Task 2
def func2(sp):
    sp = sp.split()
    stn = sp[0:1]
    year = sp[2:3]
    prcp = sp[19:20]

    l1 = prcp[0][-1]
    l2 = float(prcp[0][:-1])

    if l2 == 99.99:
        l2 = 0
    elif l1 == 'A':
        l2 = l2 * 4
    elif l1 == 'B' or l1 == 'E':
        l2 = l2 * 2
    elif l1 == 'C':
        l2 = l2 * 1.33
    year = stn + year
    year.append(str(l2))
    return (year)

log_txt = sprkctxt.textFile("file:" + str(path_for_record) + "/2006.txt")
header = log_txt.first()
fields = [StructField("STN---", StringType(), True), StructField("YEARMODA", StringType(), True), StructField("PRCP", StringType(), True)]
schema = StructType(fields)
log_txt = log_txt.filter(lambda row:row != header)
log_txt = log_txt.filter(lambda row:row.split()[19][:-1] != "99.99")

prcp_var = log_txt.map(lambda sp: func2(sp))

datafr = spark.createDataFrame(prcp_var, schema=schema)

func =  udf(lambda x: datetime.strptime(x, '%Y%m%d'), DateType())
datafr2 = datafr.withColumn('Month', date_format(func(col('YEARMODA')), 'MMMM'))
datafr2 = datafr2.withColumnRenamed("STN---", "STN")

cond = [data_locations["USAF"] == datafr2["STN"], data_locations["CTRY"] == "US", data_locations["STATE"].isNotNull()]
datafr3 = data_locations.join(datafr2, cond).select(data_locations.STATE, datafr2.STN, datafr2.PRCP, datafr2.Month)

datafr4 = datafr3.groupBy("STATE", "Month").agg({"PRCP": 'avg'})
datafr5 = datafr4.withColumn("Average_PRCP", col("avg(PRCP)"))

#Code block for Task 3
datafr8 = datafr5.orderBy('STATE', "Month")
datafr9_max = datafr8.groupBy("STATE").agg({"Average_PRCP": 'max'})
datafr9_min = datafr8.groupBy("STATE").agg({"Average_PRCP": 'min'})


cond_max = [datafr8.STATE == datafr9_max.STATE, datafr8.Average_PRCP == datafr9_max["max(Average_PRCP)"]]
cond_min = [datafr8.STATE == datafr9_min.STATE, datafr8.Average_PRCP == datafr9_min["min(Average_PRCP)"]]

datafr10_max = datafr8.join(datafr9_max, cond_max).select(datafr9_max.STATE, datafr8.Average_PRCP, datafr8.Month)
datafr10_min = datafr8.join(datafr9_min, cond_min).select(datafr9_min.STATE, datafr8.Average_PRCP, datafr8.Month)

datafr10_max = datafr10_max.withColumnRenamed("Average_PRCP", "Max_PRCP")
datafr10_max = datafr10_max.withColumnRenamed("Month", "Max_PRCP_Month")

datafr10_min = datafr10_min.withColumnRenamed("Average_PRCP", "Min_PRCP")
datafr10_min = datafr10_min.withColumnRenamed("Month", "Min_PRCP_Month")


datafr11 = datafr10_max.join(datafr10_min, datafr10_max["STATE"] == datafr10_min["STATE"]).select(datafr10_max["STATE"], datafr10_max["Max_PRCP"], datafr10_max["Max_PRCP_Month"], datafr10_min["Min_PRCP"], datafr10_min["Min_PRCP_Month"])
datafr11 = datafr11.orderBy('STATE')

#Code block for Task 4
datafr12 = datafr11.withColumn("Difference", col("Max_PRCP") - col("Min_PRCP"))

datafr13 = datafr12.orderBy('Difference')
datafr13.show(60)

datafr13.coalesce(1).write.format("csv").option("header", "true").save(str(output_loc) + "/Results.csv")

#Computing the total runtime for all the 4 tasks
stop = timeit.default_timer()
total_runtime = stop - start
print('Total Runtime: ', total_runtime)

#All the results are stored in the path specified and marks the end of the tasks.