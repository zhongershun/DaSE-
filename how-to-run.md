hadoop启动方式

```sh
docker-compose build namenode datanode1 datanode2
docker-compose up namenode datanode1 datanode2 -d

docker exec -it namenode bash

# namenode
rm -rf /usr/local/hadoop-3.3.6/tmp/namenode/*
```

```sh
docker exec -it datanode bash
#所有的datanode都要执行
rm -rf /usr/local/hadoop-3.3.6/tmp/datanode/*
chmod -R 755 /usr/local/hadoop-3.3.6/tmp/datanode
```


namende
```sh
docker exec -it namenode bash
# 数据格式化
$HADOOP_HOME/bin/hdfs namenode -format

# 启动
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh 
```


spark启动
```sh
docker-compose build spark-master spark-worker1 spark-worker2
docker-compose up spark-master spark-worker1 spark-worker2 -d
docker exec -it spark-master bash
$SPARK_HOME/sbin/start-all.sh
```

How to run mapreduce

```shell
# mapreduce

# 复制数据
docker cp ./data/cut/split_data/  namenode:/root/

# 复制代码
docker cp ./code/mapreduce_code_new namenode:/root/

# 启动
docker exec -it namenode bash
cd root
hdfs dfs -mkdir /input
hdfs dfs -put ./split_data/* /input/

# 整合代码
cd mapreduce_code_new
javac -encoding UTF-8 -classpath $(hadoop classpath) -d . PageRankMapper.java PageRankReducer.java PageRankDriver.java
jar -cvf PageRank.jar *.class	
```

```shell
hadoop jar PageRank.jar PageRankDriver /input/split_12 /output/pagerank_12  10
{}里填写full 15 12 9 6
然后运行的同时python3  monitor_new.py {}
{}里填写full 15 12 9 6
```

how to run spark

```shell
docker cp ./downloads/merged_data spark-master:/root/
```

运行时先启动pyspark,可以看到这个界面

然后将pyspark.py的代码全部复制进去，即可开始运行，运行时请启动monitor以监测性能
