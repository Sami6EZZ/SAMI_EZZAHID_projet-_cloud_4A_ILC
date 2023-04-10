from datetime import time
import datetime
import json
from flask import Flask, jsonify, request, render_template
import redis
import time

app = Flask(__name__)

db_tweet = redis.StrictRedis(host='localhost', port=6379, db=0)
db_user = redis.StrictRedis(host='localhost', port=6379, db=1)

@app.route('/')
def page_1():
    return render_template("page_1.html")

@app.route('/home' , methods=['GET'])
def home_page():
    return render_template("home.html")

@app.route('/show_all_tweets' , methods=['GET'])
def home_page1():
    return render_template("show_all_tweets.html")

@app.route('/show_tweet_byP' , methods=['GET'])
def home_page2():
    return render_template("show_tweets_byP.html")

@app.route('/show_all_h' , methods=['GET'])
def home_page3():
    return render_template("show_all_h.html")

@app.route('/show_tweets_byh' , methods=['GET'])
def home_page4():
    return render_template("show_tweets_byh.html")

@app.route('/tweet', methods=['POST'])
def save_tweet():
    author = request.json['username']
    tweet = request.json['tweet']
    sujet = request.json.get('sujet')
    timestamp = str(datetime.datetime.now())    
    tweet_data = {'timestamp' : timestamp,'username': author, 'message': tweet, 'sujet': sujet}
    db_tweet.set(timestamp, json.dumps(tweet_data))
    db_user.lpush(author, timestamp)
    return jsonify({'message': 'Tweet created successfully'})


@app.route('/tweets', methods=['GET'])
def get_all_tweets():
    tweets = []
    for tweet_key in db_tweet.keys():
        tweet = db_tweet.get(tweet_key)
        tweet_dict = json.loads(tweet.decode()) if tweet else None
        if tweet_dict:
            
            tweets.append(tweet_dict)
            

    return jsonify({'tweets': tweets})

@app.route('/tweets_by_P/<username>', methods=['GET'])
def get_tweets_by_username(username):
        # create a list to store the tweet dictionaries
    tweets = []
        # get the list of tweet timestamps for the given username from db_users
    tweet_keys = db_user.lrange(username, 0, -1)
        # loop through the tweet timestamps and get the tweet dictionaries from db_tweets
    for tweet_key in tweet_keys:
        tweet = db_tweet.get(tweet_key)
        if tweet:
            tweet_dict = json.loads(tweet.decode())
            tweets.append(tweet_dict)
    return jsonify({'tweets': tweets})

@app.route('/tweets/<string:hashtag>', methods=['GET'])
def get_tweets(hashtag):
    tweets = []
    for key in db_tweet.scan_iter():
        tweet_data = json.loads(db_tweet.get(key))
        if tweet_data and tweet_data.get('sujet') and hashtag in tweet_data.get('sujet').split():
            tweets.append(tweet_data)
    return jsonify({'tweets': tweets})


@app.route('/hashtags', methods=['GET'])
def get_hashtags():
    hashtags = set()
    for key in db_tweet.scan_iter():
        tweet_data = json.loads(db_tweet.get(key))
        if tweet_data and tweet_data.get('sujet'):
            hashtags.update(tweet_data['sujet'].split())
    return jsonify(list(hashtags))



if __name__ == '__main__':
    app.run(debug=True)