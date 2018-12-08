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

