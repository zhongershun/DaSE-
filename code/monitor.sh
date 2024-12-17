#!/bin/bash

# 输出头部
echo "TIME,CONTAINER,CPU%,MEM USAGE/LIMIT,MEM %" > docker_stats.csv

# 间隔时间（秒）
interval=3

# 提示用户启动统计
echo "按 Enter 键开始记录统计，按 Ctrl+C 停止。"
read -p "等待启动..."  # 等待用户输入

# 开始时间
start_time=$(date +%s)
echo "统计开始，按 Ctrl+C 停止记录。"

# 捕获中断信号 (Ctrl+C) 并执行清理
trap 'echo "\n统计已结束。"; exit 0' SIGINT

# 循环收集数据
while true; do
  docker stats spark-master spark-worker-1 spark-worker-2 spark-worker-3 --no-stream --format "{{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}}" |
  while read line; do
    time=$(date +%s)
    echo "$time,$line" >> docker_stats.csv
  done
  sleep $interval
done