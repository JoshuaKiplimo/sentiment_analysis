# Sentiment Analyser

First data is rerieved from twitter API by searching the term's hashtag. This data is then passed through Python's textblob, which is a library for processing textual data( I Previously used MonkeyLearn API, which I found accurate but due to limitation of number of messages that it can process at any given time, opted for Python's Textblob). In my case I used the sentiment analysis feature of textblob. The results are then passed into a dash app.



[How TextBlob works](https://sentiment-analysiss.herokuapp.com/)


As of now, the project is still in young and several updates including error handling for tweepy api, increasing accuracy of search results from the hashtags and fixing minor bugs are on the way.

### Try it

To see the sentiment analyis in action, [click here](https://sentiment-analysiss.herokuapp.com/). Allow up to 30 seconds for Heroku to start up.
