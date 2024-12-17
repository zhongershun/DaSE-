import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class PageRankMapper extends Mapper<Object, Text, Text, Text> {

    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] parts = line.split("\t");

        // 过滤掉标题行或无效行
        if (parts.length < 4 || parts[3].equals("count")) {
            System.out.println("Skipping line: " + line);
            return;
        }

        String source = parts[0]; // 来源页面
        String target = parts[1]; // 目标页面
        double weight = Double.parseDouble(parts[3]); // 跳转权重

        // 发射出链信息，用于构建图结构
        context.write(new Text(source), new Text("LINK:" + target + ":" + weight));
        System.out.println("Mapper Output (LINK): " + source + " -> LINK:" + target + ":" + weight);

        // 将权重贡献给目标页面
        context.write(new Text(target), new Text(String.valueOf(weight)));
        System.out.println("Mapper Output (Contribution): " + target + " -> " + weight);
    }
}
