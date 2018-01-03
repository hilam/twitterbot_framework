#BOT BY @TYLERGLAIEL
#@WIKIHOWDREAMS
#PICKS A RANDOM WIKIHOW IMAGE AND CAPTIONS IT WITH A RANDOM TWEET

import requests
from bs4 import BeautifulSoup
import random
import shutil
from PIL import Image
import tweepy
import time

last_chose_tweet_index = "0"
time_between_tweets = 60*60
time_between_failed_tweets = 60 #if the tweet fails (exception) how long to wait before trying again

banned_users = ["WikihowDreams"]
banned_words = ["http", "@", "&"]
punctuation = [":", ".", "?", "!"]

def get_twitter():
    CONSUMER_KEY = '123456789...'
    CONSUMER_SECRET = '123456789...'
    ACCESS_KEY = '123456789...'
    ACCESS_SECRET = '123456789...'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)

def grabimage():
    url = "http://www.wikihow.com/Special:Randomizer"
    result = requests.get(url)
    html = result.content
    soup = BeautifulSoup(html, "html.parser")

    header = soup.find_all("img", {"class": "whcdn content-fill"}, src=True)


    url = random.choice(header)['src']

    response = requests.get(url, stream=True)
    with open('temp.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

        
    img = Image.open("temp.jpg");
    img2 = img.crop((0,0,img.size[0], img.size[1]-22))
    img2.save("img.jpg")
    return "img.jpg"

def grabtweet():
    global last_chose_tweet_index
    twitter = get_twitter()
    results = twitter.search(q="\"How To\" -RT -http -https -t.co", lang="en", since_id=last_chose_tweet_index)
    
    #res = random.choice(results)
    #print(res.text)
    #print(res.id)
    for i in range(0,100):
        res = random.choice(results)
        valid = False
        text = res.text;
        
        #trim tweet down
        croptext = text[text.lower().find("how to"):]
        for p in punctuation:
            index = croptext.find(p)
            if(index != -1):
                croptext = croptext[:croptext.find(p)]
            
        #validate tweet
        #tweet must contain "how to"
        valid = True
        
        if(croptext.lower().find("how to") != 0):
            valid = False
            
        #tweet must not contain banned words
        for banned in banned_words:
            if(croptext.lower().find(banned) != -1):
                valid = False
                break
        
        #tweet must not be from banned user
        for banned in banned_users:
            if(res.user.screen_name.lower() == banned.lower()):
                valid = False
                
        if(valid):
            print(croptext)
            last_chose_tweet_index = res.id
            return croptext
    
    raise Exception("no valid tweet")
            
def make_and_send_tweet():
    twitter = get_twitter()
    image = grabimage()
    tweet = grabtweet()
    twitter.update_with_media(image, status=tweet)
    
def run_bot():
    while True:
        try:
            make_and_send_tweet()
            #sleep 1 hour
            time.sleep(time_between_tweets)
        except:
            #sleep 1 minute
            time.sleep(time_between_failed_tweets)
        
#make_and_send_tweet()
run_bot()
