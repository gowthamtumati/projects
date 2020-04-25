/* Authors : Abhishek Ayachit, Gowtham Tumati, Lovepreet Singh Dhaliwal, Sudip Bala, Teja Vemparala
 * Class : WriteTweetToMongoDB
 * Description : Hold the logic to write the crawler tweets into MongoDB
 */

package com.ir.project;

import java.io.BufferedReader;
import java.io.FileReader;
import org.bson.Document;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;


public class WriteTweetToMongoDB {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//MongoDB intilization
		BufferedReader reader;
		MongoClient mongoClient = new MongoClient("localhost", 27017);
		MongoDatabase db = mongoClient.getDatabase("tweets");
		MongoCollection tweetCollection = db.getCollection("tweetInfo");
		try {
			// Logic to read tweet by tweet and insert into MangoDB
			reader = new BufferedReader(new FileReader("/home/abc/IR/Project/InputData/CrawlerTweetDemoData.txt"));
			String line = reader.readLine();
			while (line != null) {
				line = reader.readLine();
				Document doc = Document.parse(line);
				tweetCollection.insertOne(doc);
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
