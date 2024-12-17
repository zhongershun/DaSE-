from collections import defaultdict

# 阻尼系数
DAMPING_FACTOR = 0.85

# 初始化输入文件路径
INPUT_FILE = "merged_clickstream_full.tsv"

# 迭代次数
NUM_ITERATIONS = 10

# 输出文件路径
OUTPUT_FILE = "pagerank_results.tsv"


# **Mapper 函数**
def mapper(lines):
    map_output = []
    for line in lines:
        parts = line.strip().split("\t")
        # 跳过标题行或无效行
        if len(parts) < 4 or parts[3] == "count":
            continue

        source, target, link_type, count = parts
        count = float(count)

        # 发射出链信息
        map_output.append((source, f"LINK:{target}"))

        # 发射贡献值
        map_output.append((target, str(count)))

    return map_output


# **Reducer 函数**
def reducer(mapped_data, current_ranks):
    reduced_output = defaultdict(list)

    for key, value in mapped_data:
        reduced_output[key].append(value)

    reduced_results = {}
    for key, values in reduced_output.items():
        rank_sum = 0.0
        links = []

        # 解析出链信息和贡献值
        for value in values:
            if isinstance(value, str) and value.startswith("LINK:"):
                # 解析出链
                target = value.split(":")[1]
                links.append(target)
            else:
                # 累加 PageRank 贡献值
                rank_sum += float(value)

        # 计算新的 PageRank 值
        new_rank = (1 - DAMPING_FACTOR) + DAMPING_FACTOR * rank_sum

        # 保存新的 PageRank 和出链信息
        reduced_results[key] = (new_rank, links)

    return reduced_results


# **Driver 函数**
def page_rank(input_file, output_file, num_iterations):
    # 读取输入文件
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 初始化当前页面的 PageRank 值
    current_ranks = defaultdict(lambda: 1.0)

    for iteration in range(num_iterations):
        print(f"Starting Iteration {iteration + 1}...")

        # Mapper 阶段
        mapped_data = mapper(lines)

        # Reducer 阶段
        reduced_data = reducer(mapped_data, current_ranks)

        # 准备下一次迭代的数据
        next_lines = []
        for key, (rank, links) in reduced_data.items():
            # 构建下一轮输入格式
            link_str = ",".join(links)
            next_lines.append(f"{key}\t{rank}\t{link_str}\n")

        # 更新输入数据
        lines = next_lines

        # 更新当前 PageRank
        current_ranks = {key: rank for key, (rank, _) in reduced_data.items()}

        print(f"Iteration {iteration + 1} completed.")

    # 保存最终结果到文件
        with open(output_file+str(iteration), "w", encoding="utf-8") as f:
            f.writelines(lines)

    print(f"Final results saved to {output_file}")


# **运行 PageRank 算法**
page_rank(INPUT_FILE, OUTPUT_FILE, NUM_ITERATIONS)
