#!/bin/bash

# 输出头部
echo "TIME,DISK,READ(B/s),WRITE(B/s)" > disk_io_stats.csv

# 间隔时间（秒）
interval=3

echo "按 Enter 键开始记录统计，按 Ctrl+C 停止。"
read -p "等待启动..."  # 等待用户输入

# 捕获中断信号 (Ctrl+C) 并执行清理
trap 'echo "\n统计已结束。"; exit 0' SIGINT

echo "统计开始，按 Ctrl+C 停止记录。"

# 获取初始状态
declare -A prev_read
declare -A prev_write

devices=sdc  # 获取所有磁盘设备名
for dev in $devices; do
  stats=$(cat /sys/block/$dev/stat)
  prev_read[$dev]=$(echo "$stats" | awk '{print $3}')
  prev_write[$dev]=$(echo "$stats" | awk '{print $7}')
done

# 循环统计数据
while true; do
  timestamp=$(date +%s)

  for dev in $devices; do
    stats=$(cat /sys/block/$dev/stat)
    curr_read=$(echo "$stats" | awk '{print $3}')
    curr_write=$(echo "$stats" | awk '{print $7}')

    # 计算读取和写入的速率
    read_diff=$((curr_read - prev_read[$dev]))
    write_diff=$((curr_write - prev_write[$dev]))

    # 更新上次统计值
    prev_read[$dev]=$curr_read
    prev_write[$dev]=$curr_write

    # 转换为 KB/s
    read_kbps=$((read_diff * 512 / $interval))
    write_kbps=$((write_diff * 512 / $interval))

    # 记录到 CSV 文件
    echo "$timestamp,$dev,$read_kbps,$write_kbps" >> disk_io_stats.csv
  done

  sleep $interval
done
