from pyspark.sql import SparkSession

# 阻尼系数
DAMPING_FACTOR = 0.85
# 最大迭代次数
NUM_ITERATIONS = 10
# 输入文件路径
INPUT_FILE = "./merged_data/merged_clickstream_full.tsv"
# 输出文件路径
OUTPUT_PATH = "./merged_data/res/output_pagerank_full"

# 初始化 SparkSession
spark = SparkSession.builder \
    .appName("PageRank") \
    .getOrCreate()

sc = spark.sparkContext("local","FileReader")


def parse_line(line):
    """
    解析输入数据
    :param line: 输入的一行数据
    :return: (source, (target, count)) 或 (source, [])
    """
    parts = line.strip().split("\t")
    if len(parts) < 4 or parts[3] == "count":  # 过滤标题行和无效行
        return None
    source, target, link_type, count = parts
    return source, (target, float(count))


def compute_contributions(targets, rank):
    """
    根据出链页面和 PageRank 计算贡献值
    :param targets: 出链页面列表
    :param rank: 当前页面的 PageRank 值
    :return: 每个出链页面的贡献值列表
    """
    total_targets = len(targets)
    if total_targets > 0:
        for target in targets:
            yield (target, rank / total_targets)


# 读取输入数据
lines = sc.textFile(INPUT_FILE)

# 解析输入数据，构建 RDD: (source, [(target, count)])
parsed_lines = lines.map(parse_line).filter(lambda x: x is not None)
links = parsed_lines.groupByKey().mapValues(list)

# 初始化每个页面的 PageRank 值为 1.0
ranks = links.mapValues(lambda _: 1.0)

# 开始迭代计算 PageRank
for iteration in range(NUM_ITERATIONS):
    print(f"Starting iteration {iteration + 1}...")
    # 计算每个页面对其出链页面的贡献值
    contributions = links.join(ranks).flatMap(lambda x: compute_contributions([target[0] for target in x[1][0]], x[1][1]))
    # 计算新的 PageRank 值
    ranks = contributions.reduceByKey(lambda x, y: x + y).mapValues(lambda rank: (1 - DAMPING_FACTOR) + DAMPING_FACTOR * rank)

# 最终结果：与出链信息合并
results = links.join(ranks).map(lambda x: (x[0], x[1][1], [target[0] for target in x[1][0]]))

# 将结果保存为 HDFS 或本地文件
results.map(lambda x: f"{x[0]}\t{x[1]:.4f}\t{','.join(x[2])}").saveAsTextFile(OUTPUT_PATH)

# 停止 SparkSession
spark.stop()
