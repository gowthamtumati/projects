/* Authors: Lokesh Koppaka(862123164), Abhilash Sunkam(862122847), Vishal Lella(862120385)
 * Class : InvertedIndexGenerator
 * Description : Read in the Crawled tweets and generate inverted Index.
 * 
 */

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.MultipleOutputs;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class InvertedIndexGenerator {
	
	// Mapper Class
	public static class IndexMapper extends Mapper<Object, Text, Text, Text>{
		JSONParser parser = new JSONParser();
	 public void map(Object key, Text value, Context context
	                 ) throws IOException, InterruptedException {
		 String line = value.toString();
		 Map<String, Integer> termFrequency = new HashMap<String, Integer>();
	      try
	      {
	       // Read each crawled tweet
	        Object obj = this.parser.parse(line);
	        JSONObject js = (JSONObject)obj; // Logic to convert it into JSONObject
	        String tweet = js.get("Tweet").toString(); // Logic to extract tweet
	        String hashTag = js.get("Hashtags").toString();// Logic to extract Hashtag
	        JSONObject idObj = (JSONObject)js.get("_id"); // Logic to extract documentId i.e MongoDB id here
	        String docId = (String) idObj.get("$oid");
	        // Logic to replace special character 
	        String bTweet = tweet.replaceAll("[^a-zA-Z0-9]", " ").toLowerCase();
            String bHashTag = hashTag.replaceAll("[^a-zA-Z0-9]", " ").toLowerCase();
            // Logic to split tweet text and hashtag into words
	        List<String> finalList = new ArrayList<String>();
	        List<String >words = Arrays.asList(bTweet.split("\\s+"));
	        if(bHashTag != null && !bHashTag.equals("")) {
	        	finalList.addAll(Arrays.asList(bHashTag.split("\\s+")));
	          }
	        finalList.addAll(words);
	        // Logic to compute term frequencies and construct JSON holding term frequency and docIF
	        Set<String> seenWords = new HashSet<String>();
	          for (String word : finalList) {
	        	  if(seenWords.contains(word)) {
	        		  continue;
	        	  }
	        	  int count = 0;
	        	  Pattern p = Pattern.compile(word);
	        	  Matcher m = p.matcher(bTweet + bHashTag);
	        	  while (m.find()) {
	        		  count++;
	        	  }
	        	  seenWords.add(word);
	        	  JSONObject json = new JSONObject();
	        	  json.put("docId", docId);
	        	  json.put("tf", count);
	        	  // Outputs key value pairs -> key = "word" value = "{"tf":5,"docId" = "ABC"}"
	            context.write(new Text(word), new Text(json.toString()));
	          }
	      }
	      catch (ParseException localParseException) {}
	
	 }
	}
	// Reducer Class
	public static class IndexReducer
	    extends Reducer<Text, Text, Text, NullWritable> {
	 
	 public void reduce(Text key, Iterable<Text> values,Context context) throws IOException, InterruptedException {
		 JSONObject json = new JSONObject();
		 JSONArray tweets = new JSONArray();
		 JSONParser parser = new JSONParser();
		 List<JSONObject> JSONObjectList = new ArrayList<JSONObject>();
		 // Custom comparator to sort posting list as per term frequency
		 Comparator<JSONObject> cmp = new Comparator<JSONObject>() {
		      public int compare(JSONObject o1, JSONObject o2) {
		        return -String.valueOf(o1.get("tf")).compareTo(String.valueOf(o2.get("tf")));
		      }
		 };
		 try {
			 // Logic to reduce posting list per term
			 for(Text docToTF : values) {
				 JSONObject jsonItem = (JSONObject) parser.parse(docToTF.toString());
				 JSONObjectList.add(jsonItem);
			 }
			 Collections.sort(JSONObjectList, cmp);
			 for(JSONObject tweetJson: JSONObjectList) {
				tweets.add(tweetJson);
			 }
			 json.put(key, tweets); 
			 System.out.println("Constructed json = " + json.toString());
			 // Write term along with its posting list
			 context.write(new Text(json.toString()),NullWritable.get());
		 }
		 catch (Exception e) {
			// TODO: handle exception
			 System.out.println(e.getMessage());
		}		 
	 }
	}

	public static void main(String[] args) throws Exception {
		// Basic Hadoop Map Reduce program configurations.
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "InvertedIndexing");
		job.setJarByClass(InvertedIndexGenerator.class);
		job.setMapperClass(IndexMapper.class);
		job.setReducerClass(IndexReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.setInputFormatClass(TextInputFormat.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
