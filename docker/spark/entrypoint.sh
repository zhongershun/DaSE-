#!/bin/bash
# 启动 SSH 服务
service ssh start

# 启动 Hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# 保持容器运行
tail -f /dev/null
