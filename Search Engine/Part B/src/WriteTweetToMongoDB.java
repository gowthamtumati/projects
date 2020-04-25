/* Authors : Lokesh Koppaka(862123164), Abhilash Sunkam(862122847), Vishal Lella(862120385) 
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
			reader = new BufferedReader(new FileReader("D:\\UCR\\UCR_SecondQuater_Winter2019\\InformationRetrieval\\Project\\InputData\\CrawlerTweetDemoData.txt"));
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
