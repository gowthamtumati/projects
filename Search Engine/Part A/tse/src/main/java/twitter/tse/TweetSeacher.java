package twitter.tse;

import java.io.File;
import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

public class TweetSeacher {
	
	IndexReader indexReader; // indexReader Instance - used to read the generated index
	IndexSearcher indexSearcher; // indexSearcher Instance - used to search in the generated index
	QueryParser queryParser; // queryParser Instance - used to parse user input
	 // Constructor - perform basic instantiation
	public TweetSeacher(String indexDirectoryPath) throws IOException {
			indexReader = IndexReader.open(FSDirectory.open(new File(indexDirectoryPath)));
			indexSearcher = new IndexSearcher(indexReader);
			queryParser = new QueryParser(Version.LUCENE_34, "tweet", new StandardAnalyzer(Version.LUCENE_34));
	   }
	   /* Method - search
	    * Description - parses the  searchQuery String and searches it in the index and returns Top Documents
	    */
	   public TopDocs search( String searchQuery) throws IOException, ParseException {
		  Query query = queryParser.parse(searchQuery);
	      return indexSearcher.search(query, 100);
	   }
	   /* Method - getDocument
	    * Description - return a document
	    */
	   public Document getDocument(ScoreDoc scoreDoc) throws CorruptIndexException, IOException {
	      return indexSearcher.doc(scoreDoc.doc);	
	   }
	   /* Method - closeStream
	    * Description - closes necessary streams
	    */
	   public void closeStream() throws IOException {
		   indexReader.close();
	   }

}
