def sentiment_tweet(keyword,noOfTweet):
    from textblob import TextBlob
    import sys
    import tweepy
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import os
    import nltk
    import re
    import string
    #from wordcloud import WordCloud, STOPWORDS
    from PIL import Image
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    #from nltk.sentiment.vader import SentimentIntensityAnalyzer
    #from langdetect import detect
    from nltk.stem import SnowballStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    consumer_key = '0B8LgHrv32Z2QAKpgXRcYPTkl'
    consumerSecret = 'gsYnOPacNWhO2jwQpOBaG88rD9PPadg3Fcjs0mS4FdgGKRwElH'
    accessToken = '1441259574837735427-VtzU3URvp2u19GeJN2mvd3Ga2lPAs1'
    accessTokenSecret = 'Q9XFSfW52Xx5uixrmdX9YVcusZtTYKF2zobxT7C1RRSAM'

    authenticate = tweepy.OAuthHandler(consumer_key, consumerSecret)
    authenticate.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(authenticate)

    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #keyword = input("Please enter keyword or hashtag to search: ")
    #noOfTweet = int(input ("Please enter how many tweets to analyze: "))
    tweets = tweepy.Cursor(api.search_tweets, q=keyword and "Stock", lang="en", tweet_mode = "extended").items(noOfTweet)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    obj = SentimentIntensityAnalyzer()

    tweets
    for tweet in tweets:
    
        #print(tweet.text)
        tweet_list.append(tweet.full_text)
        analysis = TextBlob(tweet.full_text)
        score = obj.polarity_scores(tweet.full_text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity
        
        if neg > pos:
            negative_list.append(tweet.full_text)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet.full_text)
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet.full_text)
            neutral += 1
    
    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)
    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')
    
    #Number of Tweets (Total, Positive, Negative, Neutral)
    tweet_list = pd.DataFrame(tweet_list, columns=['tweets'])
    #print(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    #print("total number: ",len(tweet_list))
    #print("positive number: ",len(positive_list))
    #print("negative number: ", len(negative_list))
    #print("neutral number: ",len(neutral_list))

    labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue','red']
    fig = plt.figure(figsize=(5,5))
    patches, texts = plt.pie(sizes,colors=colors, startangle=90)
    plt.style.use('default')
    plt.legend(labels)
    plt.title("Sentiment Analysis Result for keyword= "+keyword+"" )
    plt.axis('equal')
    return fig,tweet_list