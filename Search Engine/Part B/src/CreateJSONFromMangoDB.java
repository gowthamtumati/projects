/* Authors : Lokesh Koppaka(862123164), Abhilash Sunkam(862122847), Vishal Lella(862120385) 
 * Class : CreateJSONFromMangoDB
 * Description : Reads tweets from MongoDB and generates JSON per tweet holding docID, Tweet, HashTag as JSON attributes
 * 				 Note : This JSON is later used in mapReduce porgram to generate inverted index
 */
package com.ir.project;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;

import org.bson.Document;

import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class CreateJSONFromMangoDB {

	public static void main(String args[]) {
		try {
		// Logic - Establishing connection to MangoDB
		MongoClient mongoClient = new MongoClient("localhost", 27017);
		MongoDatabase db = mongoClient.getDatabase("tweets");
		// Logic - To retrieve all the tweets from the tweetInfo Collection
		MongoCollection tweetCollection = db.getCollection("tweetInfo");
		FindIterable<Document> findInterable = tweetCollection.find(new Document());
		File fout = new File("D:\\UCR\\UCR_SecondQuater_Winter2019\\InformationRetrieval\\Project\\InputData\\JsonFromMongo.txt");
		// Logic -  writes the tweets as JSON into a file 
		FileOutputStream fos = new FileOutputStream(fout);
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
		for(Document doc : findInterable) {
			bw.write(doc.toJson().toString());
			bw.newLine();
		}
		System.out.println("Completed..");
		bw.close();
		}catch (Exception e) {
			// TODO: handle exception
		}
		
	}
}
