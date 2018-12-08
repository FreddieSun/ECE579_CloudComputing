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
![](Task1/C07BD12D-9BF1-47D5-A8F9-5B32B03C9693.png)


#云计算