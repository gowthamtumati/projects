package twitter.tse;


import java.io.IOException;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import java.util.Scanner;
public class TwitterSearchEngine {
	// Constructor - instantiates necessary members
	public void createIndex(String inputPath, String outputPath) {
		try {
			TweetIndexer ti = new TweetIndexer(inputPath);
			ti.createIndex(outputPath, ".txt");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public static void main(String args[]) {
		// index generation
		if(args.length == 3 && args[2].equals("1")) {
		//if(true) {
			String inputPath = args[0]; //directory path where index file is generation
			//String directoryPath = "/Users/lavidhaliwal/Downloads/ir_project/indexed";
			String dataPath = args[1];// data file path
			//String dataPath = "/Users/lavidhaliwal/Downloads/ir_project/crawled";
			TwitterSearchEngine tse = new TwitterSearchEngine();
			long start = System.nanoTime();
			tse.createIndex(inputPath,dataPath);
			long end = System.nanoTime();
			long timeElapsed = end - start;
			System.out.println("Time Taken = " + timeElapsed/1000000 + "ms");
		}
		// search engine
		else if(args.length == 2 && args[1].equals("2")){
		//if (true) {	
		System.out.println("========================= Twitter Search Engine =========================");
			//String indexDirectory = "/Users/lavidhaliwal/Downloads/ir_project/indexed";
			String indexPath = args[0]; //directory containing index file
			Scanner sc = new Scanner(System.in); 
			System.out.println("Search Query = ");
			String query = sc.next();
			try {
				TweetSeacher ts = new TweetSeacher(indexPath);
				TopDocs topD = ts.search(query);
				System.out.println("========================= Query Results =========================");
				int rank = 1;
				for(ScoreDoc scrDoc : topD.scoreDocs) {
					System.out.println("Title = " + ts.getDocument(scrDoc).get("title"));
					System.out.println("HashTag = #" + ts.getDocument(scrDoc).get("hashTag"));
					System.out.println("Tweet = " + ts.getDocument(scrDoc).get("tweet"));
					//System.out.println("Coordinates = " + ts.getDocument(scrDoc).get("coordinates"));
					System.out.println("createdAt = " + ts.getDocument(scrDoc).get("createdAt"));
					//System.out.println("retweetCount = " + ts.getDocument(scrDoc).get("retweetCount"));
					//System.out.println("replyCount = " + ts.getDocument(scrDoc).get("replyCount"));
					System.out.println("URL = " + ts.getDocument(scrDoc).get("URL"));
					System.out.println("<== Score and Rank Info ==>");
					System.out.println("Rank = " + rank);
					System.out.println("Score = " + scrDoc.score);
					System.out.println("===========================================================================");
					rank ++;
			}
				
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		
	}

}
