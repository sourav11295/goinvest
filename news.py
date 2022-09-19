def sentiment_news(df):
    from textblob import TextBlob
    import sys
    #import tweepy
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

    def percentage(part,whole):
        return 100 * float(part)/float(whole)
    
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    news_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    obj = SentimentIntensityAnalyzer()

    for ind in df.index:
    
        #print(tweet.text)
        news_list.append(df['summary'][ind])
        analysis = TextBlob(df['summary'][ind])
        score = obj.polarity_scores(df['summary'][ind])
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity
        
        if neg > pos:
            negative_list.append(df['summary'][ind])
            negative += 1
        elif pos > neg:
            positive_list.append(df['summary'][ind])
            positive += 1
        elif pos == neg:
            neutral_list.append(df['summary'][ind])
            neutral += 1
    
    positive = percentage(positive, len(df))
    negative = percentage(negative, len(df))
    neutral = percentage(neutral, len(df))
    polarity = percentage(polarity, len(df))
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')
    
    #Number of Tweets (Total, Positive, Negative, Neutral)
    #tweet_list = pd.DataFrame(tweet_list, columns=['tweets'])
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
    plt.title("Sentiment Analysis Result" )
    plt.axis('equal')
    return fig