import tweepy
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas


class TwitterScraper:
    """
    The TwitterClient class contains all of the methods we need in order to get
    a processed tweets about a particular company or human.
    """

    def __init__(self):
        """
        initializes a TwitterScraper, goes through the necessary authentication process.
        """
        ckey = 'xxxxxx'
        csecret = 'xxxxxxx'
        atoken_key = 'xxxxxxx'
        atoken_secret = 'xxxxxxxx'
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(ckey, csecret)
            # set access token and secret
            self.auth.set_access_token(atoken_key, atoken_secret)
            # create a tweepy API object
            self.api = tweepy.API(self.auth)
        except:
            # authentication failed message
            print("Whoops! Something went wrong with authentication! ")

    def get_tweets(self, query: str, count: int = 10):
        """
        function to get all of the relevant tweets.
        :param query: the searched term
        :param count: the number of tweets we are getting
        :return: a list of tweets
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # get a count amount of tweets from query
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                # get the text from a tweet object
                text = {'text': tweet.text}

                if (tweet.retweet_count > 0 & (text not in tweets)) | (tweet.retweet_count == 0):
                    processed_tweets = self.process(text['text'])
                    unimportant_characters = set(
                        list(punctuation) + ['HANDLE', 'URL', 'rt'] + stopwords.words('english'))
                    tweets.append([word for word in processed_tweets if word not in unimportant_characters])
            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            print(str(e))

    def process(self, tweet: str):
        """
        Gets the tweet ready for analysis.
        :param tweet: the pre-processed tweet
        :return: a string that is processed
        """
        tweet = tweet.lower()  # make tweet lowercase
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove any urls
        tweet = re.sub('@[^\s]+', 'HANDLE', tweet)  # remove any twitter handles
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove any hashtags
        tweet = re.sub(r'[^a-zA-Z0-9]+', ' ', tweet)
        tweet = word_tokenize(tweet)  # removes any repeated characters and separates each word

        return tweet

    # def process(self, tweets):
    #     dataframe = pandas.DataFrame(tweets)
    #     print(dataframe.head())