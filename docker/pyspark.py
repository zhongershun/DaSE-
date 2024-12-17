from pyspark.sql import SparkSession

# 初始化 SparkSession
spark = SparkSession.builder \
    .appName("PageRank") \
    .getOrCreate()

sc = spark.sparkContext

# 输入文件路径（HDFS 或本地文件路径）
input_file = "./spark/merged_clickstream_full.tsv"

# 定义阻尼系数和迭代次数
damping_factor = 0.85
num_iterations = 10

# 读取输入数据，过滤列名
lines = sc.textFile(input_file).filter(lambda line: not line.startswith("prev_page"))

# 解析输入数据
def parse_line(line):
    parts = line.split("\t")
    if len(parts) >= 4:
        try:
            source = parts[0]
            target = parts[1]
            count = float(parts[3])
            return source, (target, count)
        except ValueError as e:
            print(f"Error parsing line: {line} -> {e}")
            return None
    else:
        print(f"Invalid line format: {line}")
        return None

# 解析数据并过滤无效行
filtered_lines = lines.map(parse_line).filter(lambda x: x is not None)

# 构建 RDD: (source, [(target1, count1), (target2, count2), ...])
links = filtered_lines.groupByKey().mapValues(list)

# 初始化 PageRank 值 (page, rank)
ranks = links.mapValues(lambda _: 1.0)

# 获取总页面数
total_pages = links.count()
total_pages_broadcast = sc.broadcast(total_pages)

# 计算跳转贡献值
def compute_contributions(targets, rank):
    total_count = sum(count for _, count in targets)
    return [(target, rank * count / total_count) for target, count in targets]

# 开始 PageRank 迭代
for i in range(num_iterations):
    # 计算每个页面对其出链页面的贡献值
    contributions = links.join(ranks).flatMap(
        lambda x: compute_contributions(x[1][0], x[1][1])
    )

    # 计算新的 PageRank 值，包含阻尼系数和孤立页面处理
    ranks = contributions.reduceByKey(lambda x, y: x + y).mapValues(
        lambda rank: (1 - damping_factor) / total_pages_broadcast.value + damping_factor * rank
    )

# 收集并排序最终的 PageRank 结果
sorted_results = ranks.sortBy(lambda x: -x[1]).collect()

# 保存结果路径（HDFS 或本地路径）
output_path = "./sorted_results"

# 保存结果到 HDFS
sc.parallelize(sorted_results).saveAsTextFile(output_path)

# 打印前 10 个结果
print("Top 10 Pages by PageRank:")
for page, rank in sorted_results[:10]:
    print(f"{page}: {rank:.5f}")

# 停止 SparkSession
spark.stop()
