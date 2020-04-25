import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import argparse
import json
import urllib2
from httplib import BadStatusLine
from lxml.html import parse
import time
import math
import re
from multiprocessing.dummy import Pool as Thread

#twitter credentials
consumer_key = "1boMBXcfavJc9fVwrW61EkQIs"
consumer_secret = "Wjibn6g0rPWWVFhWnjKdrfKHfWtoguXlD8d1nrMV40HIPPQPOK"
access_token = "3315303865-cnPF7gMKZJhSgs2sO45VOcGMR3cbqZ29uUCt4c3"
access_secret = "SSaPDleZszR4Cckm4BM036W5N20fqJ4KzFrRGkQ2YdGDH"

#arguments
dirName = str(sys.argv[1]) #data path
numTweets = int(sys.argv[2]) #num of tweets

tweetcnt = 0
filecnt = 0
file_output_path = dirName+"/tweets_data{0}.txt".format(filecnt)
f = open(file_output_path, 'a')
chkFlag = True

#twitter listener
class twitterListener(StreamListener):

    def on_connect(self):
        print (".... Connected to twitter streaming API ....")

    def on_data(self, data):
        global f
        global filecnt
        global tweetcnt
        global chkFlag

        #Checking if the file count has reached 50 (i.e 5GB)
        if (filecnt >= 50):
            print ("filecnt")
            chkFlag = False
            return False

        #Checks the number of tweets
        if tweetcnt >= numTweets and numTweets != 0:
            print ("first")
            chkFlag = False
            return False

        #Create a new text file every 50MB
        if (f.tell() >= 52428800):
            print ("last")
            f.close()
            chkFlag= True
            filecnt += 1

            file_output_path = dirName+"/tweets_data{0}.txt".format(filecnt)
            f = open(file_output_path, 'a')


        decoded = json.loads(data)

        #Get Hastags
        hashTags = decoded['entities']['hashtags']
        if (hashTags != "[]"):
            for htags in hashTags:
                hashTags = unicode(htags['text']).encode("ascii","ignore")

        #Get tweet
        tweet = unicode(decoded['text']).encode("ascii","ignore").replace('\n', ' ').replace('\t', '').replace('\r', '')

        #Get Co-ordinates
        coord = unicode(decoded['coordinates']).encode("ascii","ignore")

        #Get tweet time
        tweetTime = unicode(decoded['created_at'])

        #Get retweet count
        retweetCount = unicode(decoded['retweet_count']).encode("ascii","ignore")

        #Get reply count
        replyCount = unicode(decoded['reply_count']).encode("ascii","ignore")

        #Get favorite count
        favoriteCount = unicode(decoded['favorite_count']).encode("ascii","ignore")

        #Get URLs
        urls = unicode(decoded['entities']['urls']).encode("ascii","ignore")

        #Get title
        pageTitle = None
        expanded_url = None
        if urls != "[]":
            expanded_url = unicode(decoded['entities']['urls'][0]['expanded_url']).encode("ascii","ignore")
            try:
                page = urllib2.urlopen(expanded_url)
                p = parse(page)
                pageT = p.find(".//title")
                if (pageT != None):
                    pageTitle = unicode(p.find(".//title").text).encode("ascii","ignore")

            except urllib2.HTTPError as err:
                if err.code == 404:
                    print ("Page not found!")
                elif err.code == 403:
                    print ("Access denied!")
                else:
                    print ("Error:", err.code)
            except urllib2.URLError as err:
                print ("URL error:", err.reason)
            except BadStatusLine:
                print ("Could not fetch URL")

        if (pageTitle != None):
            pageTitle = re.sub('[^A-Za-z0-9]+', ' ', pageTitle)


        tweetData = "Hashtags:{0} Tweet:{1} Coordinates:{2} Date:{3} RetweetCount:{4} ReplyCount:{5} FavoriteCount:{6} URL:{7} Title:{8} ".format(
            hashTags, tweet, coord[36:-1], tweetTime, retweetCount, replyCount, favoriteCount, expanded_url, pageTitle)


        tweetcnt += 1
        print ('Tweet:', tweetcnt, ' F.size = ', f.tell(), ' on file:', filecnt)
        tweetData += "\n"
        print (tweetData)
        f.write(tweetData)
        return True

    def on_error(self, status):
        print (status)
        if (status == 420):
            print ("420 ERROR!!")
            return False


if __name__ == '__main__':

    while chkFlag != False:
        try:
            #Authentication and connection to twitter API
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            stream = Stream(auth, twitterListener())

            

            stream.filter(track=["#sports", "#football", "#basketball", "#cricket", "#badminton", "#tennis", "#espn","#manu","#chelsea","#Bulls","#Soccer","#WeAreACMilan","#Eagles","#FCBLive","#Patriots","#SFGiants","#gym","#workout","#nhl","#health", "#life", "#espn", "#team", "#lifestyle", "#fitnessmotivation", "#boxing","#game", "#mma","#ahletes","#motogp","#wwe","#f1","#kabaddi","#rossi", "#vettle", "#hamilton", "#rcb", "#csk", "#teamgame","#kobe","#bryant","#kobebryant", "#lakers", "#powerlifting", "#brianshaw","#mountain","#running","#tensports", "#jordan", "#mumbaiindians", "#mi", "#bhutia", "#michael", "#eddie", "#champions","#championsports", "#nike", "#nikerunning", "#adidas", "#reebok", "#bat", "#ball", "#shoes", "#injury", "#comeback", "#nba", "#superbowl", "#shakira", "#jlo","#performance","#puma", "#underarmor"])


            #Thread.map(stream)
        except Exception as e:
            print ("Exception occured: ")
            print (e)
            if (e == 420):
                waittime = 60;
                print ("Waiting for " , waittime , " seconds...")
                time.sleep(waittime)
                print ("Going")
            pass

    f.close()
