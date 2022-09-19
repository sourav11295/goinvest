import streamlit as st 
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import datetime as dt
import feedparser
from streamlit_option_menu import option_menu
import hydralit_components as hc
import time
import streamlit.components.v1 as components
from Stock_Pred import *
from tweets import *
from news import *

yf_rss_url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=IN&lang=en-US'

def get_yf_news(ticker):
    
    feed = feedparser.parse(yf_rss_url % ticker)
    
    return feed.entries

st.set_page_config(layout="centered")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

strtDate = dt.datetime.today()-dt.timedelta(days=5*365)  
endDate = dt.datetime.today() 
ticker = {
    'INFOSYS': 'INFY.NS', 'TCS': 'TCS.NS', 'WIPRO': 'WIPRO.NS', 'CIPLA': 'CIPLA.NS'
}

with st.sidebar:
    st.sidebar.header("GoInvest - Smart Investing")
    stock=st.selectbox("Choose Stock",['INFOSYS', 'TCS', 'WIPRO', 'CIPLA'])
    nav=option_menu(
        menu_title="Navigation",
        options=['About','Company Info','Financials','Stock Prediction','News','News Sentiment','Social Media','Social Sentiments'],
        icons=['info-circle','building','cash-coin','graph-up-arrow','newspaper','card-checklist','twitter','person-check-fill'],
        menu_icon='menu-button-wide-fill',
        default_index=0
    )

if nav == 'About':
    st.header("About")
    with hc.HyLoader('Loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
        time.sleep(2)
        components.html("""<div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%; padding-bottom: 48px; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFMLO6a7I8&#x2F;view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">  </iframe></div><a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFMLO6a7I8&#x2F;view?utm_content=DAFMLO6a7I8&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">""",
        height=450)


if nav == 'Company Info':
    st.header("Company Information")
    with hc.HyLoader('Loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):        
        ticker_obj = yf.Ticker(ticker[stock])  
        info = ticker_obj.get_info()
        col1, col2 = st.columns([1, 3])
        col1.subheader(info['longName'])
        col1.image(info['logo_url'],use_column_width=True)
        with col1:
            st.write("Headquarters: "+info['city'])
            st.write("Phone: +"+info['phone'])
            st.write("Country: "+info['country'])
            st.write("Zip/Pin: "+info['zip'])
            st.write("Website: "+info['website'])
            st.write("Industry: "+info['industry'])
        col2.write(info['longBusinessSummary'])

if nav == 'Financials':
    st.header("Financials")
    with hc.HyLoader('Loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
        ticker = yf.Ticker(ticker[stock])  
        data = ticker.history(start = strtDate, end = endDate)
        info = ticker.stats()
        fin = pd.DataFrame(info['financialData'].items(),columns=['parameters','value'])
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f'<p style="font-size:20px;">{"Recommendation"}</p>', unsafe_allow_html=True)
        rec = fin['value'][8].capitalize()
        col2.markdown(f'<p style="color:{"#0000FF"};font-size:20px;">{rec}</p>', unsafe_allow_html=True)
        col3.markdown(f'<p style="font-size:20px;">{"Stats Currency"}</p>', unsafe_allow_html=True)
        cur = 'INR'
        col4.markdown(f'<p style="color:{"#0000FF"};font-size:20px;">{cur}</p>', unsafe_allow_html=True)
        with col1:
            for  i in range(0,7):
                par = ''.join(map(lambda x: x if x.islower() else " "+x, fin['parameters'][i])).capitalize()
                val = fin['value'][i] 
                if val < 0:
                    col = "#FF0000"
                else:
                    col = "#008000"
                val = str("{:,}".format(val)) if val>1 else str(round(val*100,2))+'%'    
                st.write(par)
                st.markdown(f'<p style="color:{col};">{val}</p>', unsafe_allow_html=True)
        with col2:
            for  i in [x for x in range(7,15) if x != 8]:
                par = ''.join(map(lambda x: x if x.islower() else " "+x, fin['parameters'][i])).capitalize()
                val = fin['value'][i] 
                if val < 0:
                    col = "#FF0000"
                else:
                    col = "#008000"
                val = str("{:,}".format(val)) if val>1 else str(round(val*100,2))+'%'    
                st.write(par)
                st.markdown(f'<p style="color:{col};">{val}</p>', unsafe_allow_html=True)
        with col3:
            for  i in range(15,22):
                par = ''.join(map(lambda x: x if x.islower() else " "+x, fin['parameters'][i])).capitalize()
                par = par.replace("Number", 'No.')
                val = fin['value'][i] 
                if val < 0:
                    col = "#FF0000"
                else:
                    col = "#008000"
                val = str("{:,}".format(val)) if val>1 else str(round(val*100,2))+'%'    
                st.write(par)
                st.markdown(f'<p style="color:{col};">{val}</p>', unsafe_allow_html=True)
        with col4:
            for  i in [x for x in range(22,30) if x != 25]:
                par = ''.join(map(lambda x: x if x.islower() else " "+x, fin['parameters'][i])).capitalize()
                val = fin['value'][i] 
                if val < 0:
                    col = "#FF0000"
                else:
                    col = "#008000"
                val = str("{:,}".format(val)) if val>1 else str(round(val*100,2))+'%'    
                st.write(par)
                st.markdown(f'<p style="color:{col};">{val}</p>', unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=data.reset_index()['Date'],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
        fig.update_layout(
        title='Candlestick Chart',
        yaxis_title='Stock Price')
        st.plotly_chart(fig,use_container_width=True)


if nav == 'Stock Prediction':
    st.header("Stock Prediction")
    if st.button("Run Model"):
        st.warning("Please give approximately 1 min for the model to run")
        with hc.HyLoader('LSTM Model Running',hc.Loaders.standard_loaders,index=[2,2,2,2]):
            mape,rmse,fig = predict(strtDate,endDate,ticker[stock])
            st.success("Model Ran Successfully, Results are below")
            st.pyplot(fig)
            st.write("Mean Absolute Percentage Error(%): ",round(abs(mape)*100,2))
            st.write("Root Mean Squared Error: ",round(rmse,2))

if nav == 'Social Media':
    st.header("Social Media")
    noOfTweet=st.number_input("No. of Tweets(min=10,max=1000)",10,1000)
    if st.button("Fetch Tweets"):
        with hc.HyLoader('Loading Tweets',hc.Loaders.standard_loaders,index=[2,2,2,2]):
            fig, tweet_list = sentiment_tweet(stock,noOfTweet)
            for ind in tweet_list.index:
                st.info(tweet_list['tweets'][ind])


if nav == 'Social Sentiments':
    st.header("Social Sentiments")
    noOfTweet=st.number_input("No. of Tweets(min=10,max=1000)",10,1000)
    if st.button("Fetch Tweets and Analyze"):
        with hc.HyLoader('Loading Tweets',hc.Loaders.standard_loaders,index=[2,2,2,2]):
            fig, tweet_list = sentiment_tweet(stock,noOfTweet)
            for ind in tweet_list.index:
                st.info(tweet_list['tweets'][ind])
            st.pyplot(fig)

if nav == 'News':
    st.header("News")
    with hc.HyLoader('Loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
        df = pd.DataFrame(get_yf_news(ticker[stock]))
        #st.dataframe(df[['title','summary','published']])
        for ind in df.index:
            st.subheader(df['title'][ind])
            st.markdown(df['published'][ind])
            with st.expander('Expand'):
                st.markdown(df['summary'][ind])

if nav == 'News Sentiment':
    st.header("News")
    if st.button("Fetch News and Analyze"):
        with hc.HyLoader('Loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
            df = pd.DataFrame(get_yf_news(ticker[stock]))
            #st.dataframe(df[['title','summary','published']])
            for ind in df.index:
                st.subheader(df['title'][ind])
                st.markdown(df['published'][ind])
                with st.expander('Expand'):
                    st.markdown(df['summary'][ind])
            fig = sentiment_news(df)
            st.pyplot(fig)

        


