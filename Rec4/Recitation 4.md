# Recitation 4
# Task 1
## What does the code in PageRank.scala do? 

## What is the convergence criteria for PageRank in the example?

![](Recitation%204/result.png)



# Task 2 part 1


```python
sc.stop()
import pyspark
from pyspark.sql import SparkSession
sc = pyspark.SparkContext(appName="sparkSQL")
ss = SparkSession(sc)
```


```python
data = "file:////Users/weijiasun/CloudComputing18/CloudComputingRec4/Task2_problems/kddcup.data_10_percent"
raw = sc.textFile(data).cache()
```

# DataFrame
A DataFrame is a Dataset organized into named columns. It is conceptually equivalent to a table in a relational database or a data frame in R/Python, but with richer optimizations under the hood. DataFrames can be constructed from a wide array of sources such as: structured data files, tables in Hive, external databases, or existing RDDs

We want to convert our raw data into a table. But first we have to parse it and assign desired rows and headers, something like csv format. 


```python
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
from pyspark.sql import Row
```


```python
csv_data = raw.map(lambda l: l.split(","))
row_data = csv_data.map(lambda p: Row(
    duration=int(p[0]), 
    protocol_type=p[1],
    service=p[2],
    flag=p[3],
    src_bytes=int(p[4]),
    dst_bytes=int(p[5])
    )
)
```

Once we have our RDD of Row we can infer and get a schema. We can operate on this schema with SQL queries.


```python
kdd_df = sqlContext.createDataFrame(row_data)
kdd_df.registerTempTable("KDDdata")
```


```python
# Select tcp network interactions with more than 2 second duration and no transfer from destination
tcp_interactions = sqlContext.sql("SELECT duration, dst_bytes FROM KDDdata WHERE protocol_type = 'tcp' AND duration > 2000 AND dst_bytes = 0")
tcp_interactions.show(10)
```

    +--------+---------+
    |duration|dst_bytes|
    +--------+---------+
    |    5057|        0|
    |    5059|        0|
    |    5051|        0|
    |    5056|        0|
    |    5051|        0|
    |    5039|        0|
    |    5062|        0|
    |    5041|        0|
    |    5056|        0|
    |    5064|        0|
    +--------+---------+
    only showing top 10 rows
    



```python
# Complete the query to filter data with duration > 2000, dst_bytes = 0. 
# Then group the filtered elements by protocol_type and show the total count in each group.
# Refer - https://spark.apache.org/docs/latest/sql-programming-guide.html#dataframegroupby-retains-grouping-columns

kdd_df.select("protocol_type", "duration", "dst_bytes").filter(kdd_df.duration>2000)#.more query...
```




    DataFrame[protocol_type: string, duration: bigint, dst_bytes: bigint]




```python
def transform_label(label):
    '''
    Create a function to parse input label
    such that if input label is not normal 
    then it is an attack
    '''
    


row_labeled_data = csv_data.map(lambda p: Row(
    duration=int(p[0]), 
    protocol_type=p[1],
    service=p[2],
    flag=p[3],
    src_bytes=int(p[4]),
    dst_bytes=int(p[5]),
    label=transform_label(p[41])
    )
)
kdd_labeled = sqlContext.createDataFrame(row_labeled_data, samplingRatio=0.5)

'''
Write a query to select label, 
group it and then count total elements
in that group
'''
# query
```




    '\nWrite a query to select label, \ngroup it and then count total elements\nin that group\n'



We can use other dataframes for filtering our data efficiently.


```python
kdd_labeled.select("label", "protocol_type", "dst_bytes").groupBy("label", "protocol_type", kdd_labeled.dst_bytes==0).count().show()
```

    +-----+-------------+---------------+------+
    |label|protocol_type|(dst_bytes = 0)| count|
    +-----+-------------+---------------+------+
    | null|          tcp|          false| 70169|
    | null|          udp|          false| 15594|
    | null|          tcp|           true|119896|
    | null|          udp|           true|  4760|
    | null|         icmp|           true|283602|
    +-----+-------------+---------------+------+
    


It can be inferred that we have large number of tcp attacks with zero data transfer = 110583 as compared to normal tcp = 9313.

This type of analysis is known as [exploratory data analysis](http://www.stat.cmu.edu/~hseltman/309/Book/chapter4.pdf)

## Task 2 part 2


```python
sc.stop()
import pyspark
from pyspark.sql import SparkSession
sc = pyspark.SparkContext(appName="sparkSQL")
ss = SparkSession(sc)
```


```python
data = "file://///Users/weijiasun/CloudComputing18/ECE579_CloudComputing/Rec4/CloudComputingRec4/Task2_problems/kddcup.data_10_percent"
raw = sc.textFile(data).cache()
```

We will create a local dense vector for our KDD dataset.


```python
raw.take(1)
```

    [u'0,tcp,http,SF,181,5450,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,9,9,1.00,0.00,0.11,0.00,0.00,0.00,0.00,0.00,normal.']

```python
import numpy as np

def parse_kdd(line):
    split = line.split(",")
    # we will keep just numeric and logical values
    # discard any string values
    symbolic_indexes = [1,2,3,41]
    clean_split = [item for i,item in enumerate(split) if i not in symbolic_indexes]
    return np.array([float(x) for x in clean_split])

vector_data = raw.map(parse_kdd)
```


```python
from pyspark.mllib.stat import Statistics 
from math import sqrt 

# Compute column summary statistics.
summary = Statistics.colStats(vector_data)

print "Duration Statistics:"
print " Mean: {}".format(round(summary.mean()[0],3))
print " St. deviation: {}".format(round(sqrt(summary.variance()[0]),3))
print " Max value: {}".format(round(summary.max()[0],3))
print " Min value: {}".format(round(summary.min()[0],3))
print " Total value count: {}".format(summary.count())
print " Number of non-zero values: {}".format(summary.numNonzeros()[0])

```

    Duration Statistics:
     Mean: 47.979
     St. deviation: 707.746
     Max value: 58329.0
     Min value: 0.0
     Total value count: 494021
     Number of non-zero values: 12350.0


We are interested in preparing a classification system for attack/no attack or different attack types. This requires us to use label along with summary statistics and analyse data properly. 


```python
# Create a function to return a tuple with label as its zeroth index 
# and corresponding summary statistic as its first index. 
def parse_kdd_label(line):
    split = line.split(",")
    # we will keep just numeric and logical values
    # discard any string values
```


```python
def summary_by_label(raw_data, label):
    label_vector_data = raw_data.map(parse_kdd_label).filter(lambda x: x[0]==label)
    return Statistics.colStats(label_vector_data.values())
```


```python
label_list = ["back.","buffer_overflow.","ftp_write.","guess_passwd.",
              "imap.","ipsweep.","land.","loadmodule.","multihop.",
              "neptune.","nmap.","normal.","perl.","phf.","pod.","portsweep.",
              "rootkit.","satan.","smurf.","spy.","teardrop.","warezclient.",
              "warezmaster."]
```


```python
label_summary_dict = {}
# Create a dictionary of key = label_list elements, value = corresponding summary statistics 
```


```python
print label_summary_dict['pod.']
```


#云计算