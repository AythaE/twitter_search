# twitter_search
Python program to recover tweets and export it to `.csv`. It uses [Tweepy](https://github.com/tweepy/tweepy) to handle Twitter API. The script create 3 files:
- `queryX_(dateSince_dateUntil)_Tweets.csv`: Contains the Tweet text and id, the creation date, the user that wrote it and some info about him/her.
- `queryX_(dateSince_dateUntil)_Users.csv`: Contains the same user data than the previous file but without duplicated users. It is prepared to be imported into [Gephi](https://gephi.org/) as a nodes table spreadsheet.
- `queryX_(dateSince_dateUntil)_Edges.csv`: Contains the relationships between tweets (retweets and mentions). It is prepared to be imported into [Gephi](https://gephi.org/) as a edges table spreadsheet.

To use this program you need to register a Twitter application to get the required credentials and insert it on the file [`credentials.py`](credentials.py).

## Tutorial
A complete tutorial for this could be found [here](https://thebrickinthesky.wordpress.com/2014/06/26/maths-with-python-6-twitter-api-tweepy-for-social-media-and-networks-with-gephi/).

## Use
You need to install Python 3 and `virtualenv` before use this program. When this is done you could install the rest of the dependencies executing the next commands (the commands could be different in your OS):

```
virtualenv -p$(which python3) venv
source venv/bin/activate
pip install -r requirements.txt
```

And run the script with:

```
python twitter_search.py
```
