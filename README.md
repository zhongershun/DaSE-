# DaSE-
2024秋季学习DaSE大规模数据处理课程小组作业


数据集介绍：

Wikipedia Clickstream 数据集

数据集介绍（简单介绍）

```shell
<referer>	<resource>	<type>	<count>

```



实验设计

系统结构
1. HDFS（Hadoop Distributed File System）
NameNode：

HDFS的主节点，负责管理文件系统的命名空间和控制对文件的访问。
在集群中只有一个NameNode，它存储了文件系统的元数据和所有文件、目录的树状结构。
DataNode：

HDFS的工作节点，负责存储实际的数据块。
在设计方案中，我们有两个DataNode，它们会存储文件数据块，并定期向NameNode报告自己的状态和所存储的数据块。
<!-- 2. YARN（Yet Another Resource Negotiator）
ResourceManager：

YARN的全局资源管理器，负责整个集群的资源分配和调度。
在设计方案中，ResourceManager运行在与NameNode相同的节点上，这是因为ResourceManager需要与NameNode紧密协作，以获取集群的资源使用情况。
NodeManager：

YARN的工作节点，负责管理单个节点上的资源和任务的监控。
在设计方案中，我们有两个NodeManager，它们运行在与DataNode相同的节点上，这意味着每个节点既是HDFS的数据存储节点，也是YARN的计算节点。 -->
3. MapReduce
MapReduce作业运行在YARN提供的容器中，这些容器由ResourceManager分配和管理。
MapReduce的两个主要组件是Map任务和Reduce任务，它们分别在YARN的NodeManager上运行。
MapReduce框架负责处理作业的调度和监控，以及任务的执行。



1. Spark Master节点
Master：
Spark集群的管理和控制节点，负责资源分配、任务调度和集群管理。
Master节点运行Spark的Master进程，它负责监控集群状态，分配资源给各种Spark作业，并跟踪作业的执行进度。
2. Spark Worker节点
Worker：
Spark的工作节点，负责执行Spark作业中的任务。
每个Worker节点运行一个Worker进程，它们向Master注册，提供节点的资源信息，并接收Master分配的任务。
Worker节点还负责执行实际的任务，如Map、Reduce、Aggregate等，并返回结果给Master。



s实验环境




实验流程


部署启动docker

docker
v24.0.7

docker-compose
v2.31.0

hadoop 3.3.6
spark 3.5.3

hadoop启动方式

```sh
docker-compose build
docker-compose up -d

docker exec -it namenode bash

# #namenode
# chmod -R 755 /usr/local/hadoop-3.3.6/tmp/namenode
# #datanode
# chmod -R 755 /usr/local/hadoop-3.3.6/tmp/datanode

```


namende
```sh
# 数据格式化
$HADOOP_HOME/bin/hdfs namenode -format

# 启动
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh 
```



实验结果

实验总结