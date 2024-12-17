import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class PageRankDriver extends Configured implements Tool {

    @Override
    public int run(String[] args) throws Exception {
        if (args.length < 3) {
            System.err.println("Usage: PageRankDriver <input_path> <output_path> <num_iterations>");
            return -1;
        }

        String inputPath = args[0];
        String outputPath = args[1];
        int numIterations = Integer.parseInt(args[2]);

        for (int i = 0; i < numIterations; i++) {
            Job job = Job.getInstance(getConf(), "PageRank Iteration " + (i + 1));
            job.setJarByClass(PageRankDriver.class);

            job.setMapperClass(PageRankMapper.class);
            job.setReducerClass(PageRankReducer.class);

            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            FileInputFormat.addInputPath(job, new Path(inputPath));
            FileOutputFormat.setOutputPath(job, new Path(outputPath + "_iter" + (i + 1)));

            if (!job.waitForCompletion(true)) {
                System.err.println("Job failed at iteration " + (i + 1));
                return 1;
            }

            // 更新输入路径为本次输出路径
            inputPath = outputPath + "_iter" + (i + 1);
        }
        return 0;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new Configuration(), new PageRankDriver(), args);
        System.exit(exitCode);
    }
}
