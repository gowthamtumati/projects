/* Authors : Abhishek Ayachit, Gowtham Tumati, Lovepreet Singh Dhaliwal, Sudip Bala, Teja Vemparala
 * Class : SearchLuceneIndex
 * Description : REST API exposes the following methods
 * 				 /lucene/{keyword} - returns Lucene results as JSON
 * 				 /hadoop/{keyword} - returns Hadoop results as JSON
 * 				 /test 			   - returns text, this is test method for testing the service
 */
package com.ir.project;
import java.awt.PageAttributes.MediaType;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import javax.ws.rs.*;
import javax.ws.rs.core.*;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.ResponseBuilder;

import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

@Path("/search")
public class SearchLuceneIndex
{
	private MongoClient mongoClient;
	private MongoDatabase db;
	private MongoCollection tweetCollection;
	private JSONObject invertedJson;
	// Constructor - initialization of Database and Loads inverted index
  public SearchLuceneIndex() {
	  // Initialize Database
	  mongoClient = new MongoClient("localhost", 27017);
	  db = mongoClient.getDatabase("tweets");
	  tweetCollection = db.getCollection("tweetInfo");
	  // Logic to load InvertedIndex JSON
	  JSONParser parser = new JSONParser();
	  try {
	  Object obj = parser.parse(new FileReader("/home/abc/IR/Project/OutputFiles/bigJSON.txt")); // Add file Name here!
	  invertedJson = (JSONObject)obj;
	  System.out.println("Data is loaded !!");
	  }catch (Exception e) {
		// TODO: handle exception
		 System.out.println("Exception during construction :: " + e);
	}

  }
  // GET METHOD - returns query results from Lucene as json
  @GET
  @Path("/lucene/{keyword}")
  @Produces("application/json")
  public List<TweetResponse> searchLucene(@PathParam("keyword") String keyword)
  {
    try
    {
      long startTime = System.nanoTime();
      String indexDirectory = "/home/abc/IR/Project/IndexedFiles";
	  TweetSearcher indexSearcher = new TweetSearcher(indexDirectory);
	  TopDocs topD = indexSearcher.search(keyword);
	  List<TweetResponse> responseStr = new ArrayList<TweetResponse>();
	  for(ScoreDoc scrDoc : topD.scoreDocs) {
		  TweetResponse tweetRes = new TweetResponse(indexSearcher.getDocument(scrDoc).get("title"), indexSearcher.getDocument(scrDoc).get("hashTag"), indexSearcher.getDocument(scrDoc).get("tweet"), indexSearcher.getDocument(scrDoc).get("createdAt"), indexSearcher.getDocument(scrDoc).get("URL"),indexSearcher.getDocument(scrDoc).get("coordinates"));
		  responseStr.add(tweetRes);
	  }
	  long stopTime = System.nanoTime();
	  System.out.println("Time Taken for Lucene= " + (stopTime - startTime)/1000000 + "millSec");
	  return responseStr;
    }
    catch (Exception e)
    {
    	System.out.println(e);
    }
    return null;
  }
  // GET METHOD - returns query results from hadoop as json
  @GET
  @Path("/hadoop/{keyword}")
  @Produces("application/json")
  public List<TweetResponse> searchHadoop(@PathParam("keyword") String keyword)
  {
	  String queryString = keyword; // Holds query string
	  System.out.println(keyword);
	  keyword = keyword.toLowerCase(); // Logic to convert to LowerCase
	  String[] queryWords = keyword.split("\\s+");
	  System.out.println("Size = " + queryWords.length);
	  Map<String, Double> documentToTF = new TreeMap<String, Double>(); // Holds docId to Term Frequency
	  Map<String, TweetResponse> documentToInstance = new HashMap<String, TweetResponse>(); // Holds docId to TweetResponse
	  List<TweetResponse> responseStr = new ArrayList<TweetResponse>(); // Holds query results
	  JSONParser parser = new JSONParser();
	  try {
		  long startTime = System.nanoTime();
	  for(String queryWord: queryWords) {
		  	if(invertedJson.get(queryWord) != null) {
		  		JSONArray postingList = (JSONArray) parser.parse((String)invertedJson.get(queryWord));
		  		int df =  postingList.size();
		  		for (int i = 0; i < df; i++) {
		  			JSONObject jsonObjectRow = (JSONObject)postingList.get(i);
		  			String docId = jsonObjectRow.get("docId").toString();
		  			int tf = Integer.valueOf(jsonObjectRow.get("tf").toString());
		  			double idf = Math.log10(311269/df);
		  			double score = tf * idf;
		  			// Logic to build Map of docId to score
		  			if(documentToTF.containsKey(docId)) {
		  				double existingScore = documentToTF.get(docId);
		  				score +=existingScore;
		  			}
		  			documentToTF.put(docId, score);
		  			// Logic to build Map of docId to TweetResponse
		  			BasicDBObject query = new BasicDBObject();
				    query.put("_id", new ObjectId(docId));
		  			FindIterable<Document> itr = tweetCollection.find(query);
					for(Document d : itr) {
						// Logic to create an instance of TweetResponse
						Object obj = parser.parse(d.toJson().toString());
						JSONObject tweetJson = (JSONObject)obj;
						TweetResponse tr = new TweetResponse(tweetJson.get("Title").toString(),tweetJson.get("Hashtags").toString(), tweetJson.get("Tweet").toString(), tweetJson.get("Date").toString(), tweetJson.get("URL").toString(), tweetJson.get("Coordinates").toString());
						documentToInstance.put(docId, tr);
					}

		  		}
		  	}
	  }
	  // sorts the results by score
	  Map sortedMap = sortByValues(documentToTF);
	  int limit = 0;
	  for(String docId: documentToTF.keySet()) {
		  responseStr.add(documentToInstance.get(docId));
		  if(limit == 100) {
			  break;
		  }
		  limit ++;
	  }
	  long stopTime = System.nanoTime();
	  System.out.println("Time Taken for Hadoop = " + (stopTime - startTime)/1000000 + "millSec");
	  } catch (Exception e) {
		System.out.println(e);
	}
	  return responseStr;
  }
// Custom Comparator sort search based on Score
 public static <K, V extends Comparable<V>> Map<K, V> sortByValues(final Map<K, V> map) {
  Comparator<K> valueComparator = new Comparator<K>() {
    public int compare(K k1, K k2) {
      int compare = -map.get(k1).compareTo(map.get(k2));
      if (compare == 0)
        return 1;
      else
        return compare;
    }
  };
  Map<K, V> sortedByValues = new TreeMap<K, V>(valueComparator);
  sortedByValues.putAll(map);
  return sortedByValues;
}
  @GET
  @Path("/test")
  @Produces("application/json")
  public String test()
  {
    return "hello world";
  }
}
