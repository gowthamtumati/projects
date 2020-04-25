/* Authors : Lokesh Koppaka(862123164), Abhilash Sunkam(862122847), Vishal Lella(862120385) 
 * Class : TweetResponse
 * Description : Class template for Tweet Response
 */

package com.ir.project;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
public class TweetResponse {
	public String title;
	public String hashTag;
	public String tweet;
	public String createdAt;
	public String URL;
	public String coordinates;
	public TweetResponse() {
		
	}
	public TweetResponse(String title, String hashTag, String tweet, String createdAt, String URL, String coordinates){
		this.title = title;
		this.hashTag = hashTag;
		this.tweet = tweet;
		this.createdAt = createdAt;
		this.URL = URL;
		this.coordinates = coordinates;
	}
	public String getTitle() {
		return title;
	}
	public String getHashTag() {
		return hashTag;
	}
	public String getTweet() {
		return tweet;
	}
	public String getCreatedAt() {
		return createdAt;
	}
	public String getURL() {
		return URL;
	}
	public String getCoordinates() {
		return coordinates;
	}
}
