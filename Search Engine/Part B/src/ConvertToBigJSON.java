/* Authors : Lokesh Koppaka(862123164), Abhilash Sunkam(862122847), Vishal Lella(862120385) 
 * Class : ConvertToBigJSON
 * Description : Reads generated inverted index JSON from Hadoop and generates a Big JSON.
 * 				 Note: This Big JSON of inverted index is later used during the search process for fast retrieval of records from MongoDB
 */

package com.ir.project;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class ConvertToBigJSON {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Map<String, String> jsonMap = new HashMap<String, String>(); // jsonMap - used in constructing big JSON
		JSONParser parser = new JSONParser();
		JSONObject Json = null;
		BufferedReader reader;
		try {
			// Read the file holding JSON at each line
			reader = new BufferedReader(new FileReader("D:\\UCR\\UCR_SecondQuater_Winter2019\\InformationRetrieval\\Project\\OutputFiles\\part-r-000002"));
			String line = reader.readLine();
			while (line != null) {
				Object obj = parser.parse(line);
				Json = (JSONObject)obj;
				for(Object key : Json.keySet()) {
					if(!key.toString().trim().equals("")) {
						jsonMap.put(key.toString().trim(), Json.get(key).toString());
					}
				}
				line = reader.readLine();
			}
			reader.close();
			// Write the Map as Big JSON into a file
			BufferedWriter writer = new BufferedWriter(new FileWriter("D:\\UCR\\UCR_SecondQuater_Winter2019\\InformationRetrieval\\Project\\OutputFiles\\bigJSON.txt"));
		    JSONObject.writeJSONString(jsonMap, writer);
		    writer.close(); 
		    System.out.println("Completed!");		
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

}
