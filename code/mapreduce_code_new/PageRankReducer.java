import java.io.IOException;
import java.util.ArrayList;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class PageRankReducer extends Reducer<Text, Text, Text, Text> {
    private static final double DAMPING_FACTOR = 0.85;

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        ArrayList<String> links = new ArrayList<>();
        double rankSum = 0.0;

        System.out.println("Reducer Key: " + key.toString()); // 输出当前处理的 Key

        for (Text value : values) {
            String val = value.toString();

            if (val.startsWith("LINK:")) {
                // 解析出链目标和权重
                String[] linkParts = val.substring(5).split(":");
                if (linkParts.length == 2) {
                    String target = linkParts[0];
                    String weight = linkParts[1];
                    links.add(target + ":" + weight);
                }
                System.out.println("Reducer Found LINK: " + val);
            } else {
                // 累加来自其他页面的 PageRank 贡献值
                try {
                    rankSum += Double.parseDouble(val);
                    System.out.println("Reducer Contribution: " + key.toString() + " += " + val);
                } catch (NumberFormatException e) {
                    System.err.println("Reducer Invalid Contribution: " + val);
                }
            }
        }

        // 计算新的 PageRank 值
        double newRank = (1 - DAMPING_FACTOR) + DAMPING_FACTOR * rankSum;

        // 输出新的 PageRank 值和出链信息
        String output = newRank + "\t" + String.join(",", links);
        context.write(key, new Text(output));
        System.out.println("Reducer Output: " + key.toString() + " -> " + output);
    }
}
