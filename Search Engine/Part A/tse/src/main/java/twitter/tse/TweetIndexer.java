package twitter.tse;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

public class TweetIndexer {
	   private IndexWriter writer;
	   // Constructor - peforms indexWriter instantiation
	   public TweetIndexer(String indexPath) throws IOException {		 
	      Directory indexDirectory = FSDirectory.open(new File(indexPath));
	      IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_34, new StandardAnalyzer(Version.LUCENE_35));
	      writer = new IndexWriter(indexDirectory, config);
	   }
	   /* 
	    * Method - getDocument
	    * Description - Reads in tweet and return Document instance
	    */
	   private Document getDocument(String tweetRecord) throws IOException {
	      Document document = new Document();
	      int[] indexList = new int[9];
	      indexList[0] = tweetRecord.indexOf(" Tweet:");
	      indexList[1] = tweetRecord.indexOf(" Coordinates:");
	      indexList[2] = tweetRecord.indexOf(" Date:");
	      indexList[3] = tweetRecord.indexOf(" RetweetCount:");
	      indexList[4] = tweetRecord.indexOf(" ReplyCount:");
	      indexList[5] = tweetRecord.indexOf(" FavoriteCount:");
	      indexList[6] = tweetRecord.indexOf(" URL:");
	      indexList[7] = tweetRecord.indexOf(" Title:");
	      /* Logic to parse the tweet and add fields to the document */
	      document.add(new Field("hashTag", tweetRecord.substring(9,indexList[0]),Field.Store.YES,Field.Index.ANALYZED));
	      document.add(new Field("tweet", 	tweetRecord.substring(indexList[0] + 7,indexList[1]),Field.Store.YES,Field.Index.ANALYZED));
	      document.add(new Field("coordinates", tweetRecord.substring(indexList[1] + 13,indexList[2]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("createdAt", tweetRecord.substring(indexList[2] + 7,indexList[3]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("retweetCount", tweetRecord.substring(indexList[3] + 14,indexList[4]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("replyCount", tweetRecord.substring(indexList[4] + 12,indexList[5]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("FavoriteCount", tweetRecord.substring(indexList[5] + 15,indexList[6]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("URL", tweetRecord.substring(indexList[6] + 5,indexList[7]),Field.Store.YES,Field.Index.NO));
	      document.add(new Field("title", tweetRecord.substring(indexList[7] + 7,tweetRecord.length()),Field.Store.YES,Field.Index.NO));
	      return document;
	   } 
	   /* Method - indexFile
	    * Description - reads all the tweets and generates index files
	    */
	   private void indexFile(File file) throws IOException {
		  BufferedReader reader;
		  try {
			   reader = new BufferedReader(new FileReader(file));
			   String line = reader.readLine();
			   // Logic to read each line from the file and generate index
			   while(line != null) { 
				   Document document = getDocument(line);
				   writer.addDocument(document);
				   line = reader.readLine();
			   }
			   reader.close();
		  }
		  catch(Exception e) {
			  //System.out.println("Error -- " + e);
		  }
	      
	   }
	   /* Method - createIndex
	    * Description - reads all files in that directory passed in and passes it to indexFile File to generate Index
	    */
	   public int createIndex(String dataDirPath, String filter) 
	      throws IOException {
	      //get all files in the data directory
	      File[] files = new File(dataDirPath).listFiles();
	      for (File file : files) {
	         if(!file.isDirectory()
	            && !file.isHidden()
	            && file.exists()
	            && file.canRead()
	            && file.getName().toLowerCase().endsWith(filter)
	         ){
	        	 System.out.println("================Indexing Started================");
	            indexFile(file);
	            System.out.println("================Indexing Ended================");
	            
	         }
	      }
	      int num = writer.numDocs();
	      writer.close();
	      return num;
	      
	   }
}
