# twitter_search
Python program to recover tweets and export it in [Gephi](https://gephi.org/).

It uses [Tweepy](https://github.com/tweepy/tweepy) to handle Twitter API.

To use this program you need to register a Twitter application to get the required credentials

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
