from TwitterScraper import TwitterScraper


def main():
    # creates a TwitterScraper instance and prints out some tweets.
    api = TwitterScraper()
    tweets = api.get_tweets('donald trump', 5)
    print(tweets[0:5])
    # structured_tweet = api.process(tweets)
    # print(structured_tweet)


# searched_words = input("Enter a person or company to check:")
main()
