# Recitation 3
# Task1

```shell
> bin/zookeeper-server-start.sh config/zookeeper.properties

> bin/kafka-server-start.sh config/server.properties

> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

Then you can send the msg from the producer to the consumer.

> $SPARK_HOME/bin/spark-submit $SPARK_HOME/examples/src/main/python/streaming/network_wordcount.py localhost 9999

> nc -lk 9999
hello world, this is weijia sun from ece 579 cloud compuing


```
![](https://github.com/FreddieSun/ECE579_CloudComputing/blob/master/Rec3/screenshots/Task1.png)


# Task2
## Q1: What does the below part of the makefile do?
The below part of code lists the required files for MapReduce mapper, combiner and reducer and set `mmm-map.py,` `mmm-combiner.py` , `mmm-reduce.py` as the input file for mapper, combiner and reduce, and then set the input directory and output directory as defined at the begining. At last the commands print the content of mmm file to show the result.

## Q2: What is the output mmm?
 The output mmm file stores the min, max and mean key-value pairs as the result of MapReduce. 

### Q3: What does mmm-map do?
`mmm-map `turn every input content into three key-value pairs as min x.xxx, max x.xxx and mean x.xxx.

### Q4: What does the for-loop in mmm-combiner do?
mmm-combiner updates the xmax and xmin from key max and min, and add the sum of every content as well as count the number of total content for futher calculation of mean, output processed key-value pairs as min, max and mean.

mmm-reducer continue finish the update task which may not be finished by combiner, and then calculate the mean according to xsum and count.

## Q5: Can the mmm-combiner code be replaced with the code in mmm-reducer? Why?
mmm-reducer continue finish the update task which may not be finished by combiner, and then calculate the mean according to xsum and count.

I don't think combiner's code can be replaced by reducer's because combiner is not guaranteed to launch as job is busy. If replaced and one of the combiner did't work, the calculated value of mean would be wrong. A combiner should function as a optimizer to save the network transmission and shall not impact the final output. 

## hist-map.py

```python
#!/usr/bin/env python
import sys
import numpy

### Prevents pipe IO errors for large files.
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
###

# read parameters from distributed cache - nbins, minmeanmax
f = open('nbins','r') # read nbins file
params = f.readline().strip().split() # read nbins file
nbins = int(params[0]) # set maximum number of bins
f.close()

f = open('mmm','r') # open mmm file

'''
Read mmm file and assign min, max and mean values.
File read operation in similar to above reading procedure.
'''
params =  f.readline().strip().split()
xmax = float(params[1]) 
params = f.readline().strip().split()
xmean = float(params[1])
params = f.readline().strip().split()
xmin = float(params[1])
f.close()



dx = (xmax-xmin)/nbins # bin width calculation


# compute bin centre
#### complete this code
for line in sys.stdin:
    line = line.strip()

    words = line.split()
    x = float(words[0])
    if xmax-x<=0 :
        bn = int((x-xmin)/dx)-1
    else:
        bn = int((x-xmin)/dx)
    bc = bn * dx + xmin +dx/2
    strbc = str(bc)


# process input data
#### complete this code
    print '%s\t%d' %(strbc,1);

```

## hist-combine-reduce.py
```python
#!/usr/bin/env python
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

count = 0
currentKey = None

#### Complete the rest of the code

def updateResults(value, count): 
    scount = value      
    newcount = int(scount)
    count += newcount
    return (count)

def printResults(key, count):
    if key:
        print '%s\t%d' % (key, count);


for line in sys.stdin:
    line = line.strip()

    key, value = line.split('\t',1)
    
    if currentKey == key:
        count = updateResults(value, count)
       # count += int(value);
    else:
        printResults(currentKey, count)
        currentKey = key;
       # count = int(value);
        count = updateResults(value, 0)

printResults(currentKey, count)
```
