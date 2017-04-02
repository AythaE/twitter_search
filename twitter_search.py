# -*- coding: utf-8 -*-
import csv
import datetime
import json
import time

import tweepy
from credentials import *


def connectTwitterAPI():
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  return api


def printsMenu():
  print("\nTwitter_search\n")
  print("Recover tweets of some topic between 2 dates and export it into .csv files to be imported in Gephi")

  print("\nAuthor: Aythami Estévez Olivas <aythae [at] gmail [dot] com>")
  print("Repository: https://github.com/AythaE/GIW")

  print("\n\n")
  searchQuery = input("Insert the search query to look for tweets: ")
  tweetNum = input("Choose the number of tweets to recover: ")
  since = input(
      "Insert the first creation date of the tweets to recover formatted as YYYY-MM-DD (no more than 7 days before now)[Leave empty for not limit]: ")
  until = input(
      "Insert the last creation date of the tweets to recover formatted as YYYY-MM-DD (no more than 7 days before now)[Leave empty for not limit]: ")
  lang = input(
      "Insert the desire language for the tweets (given by an ISO 639-1): ")

  print()

  totalTweets = recoverTweets(
      searchQuery, int(tweetNum), since, until, lang)

  print()

  today = datetime.date.today()

  csvTweets = searchQuery

  if (since is not "") | (until is not ""):
    if since is not "":
      csvTweets += "_(" + since
    if until is not "":
      csvTweets += "_" + until
    csvTweets += ")_Tweets.csv"
  else:
    csvTweets += "_(" + str(today.day) + "-" + \
        str(today.month) + "-" + str(today.year) + ")_Tweets.csv"
  print("Saving tweets to " + csvTweets)
  saveTweetsToCSV(totalTweets, csvTweets)

  csvUsers = searchQuery

  if (since is not "") | (until is not ""):
    if since is not "":
      csvUsers += "_(" + since
    if until is not "":
      csvUsers += "_" + until
    csvUsers += ")_Users.csv"
  else:
    csvUsers += "_(" + str(today.day) + "-" + \
        str(today.month) + "-" + str(today.year) + ")_Users.csv"
  print("Saving tweets users to " + csvUsers)
  saveTweetsUsersToCSV(totalTweets, csvUsers)

  csvEdges = searchQuery

  if (since is not "") | (until is not ""):
    if since is not "":
      csvEdges += "_(" + since
    if until is not "":
      csvEdges += "_" + until
    csvEdges += ")_Edges.csv"
  else:
    csvEdges += "_(" + str(today.day) + "-" + \
        str(today.month) + "-" + str(today.year) + ")_Edges.csv"

  print("Saving tweets relationships to " + csvEdges)
  saveTweetRelationshipsToCSV(totalTweets, csvEdges)

  print("\nTo import them in Gephi, import the Users.csv as a nodes table spreadsheet and the Edges.csv as edges table spreadsheet")
  return


def recoverTweets(searchQuery, numTweets, since, until, lang):
  '''
   'searchQuery': Search query to recover tweets
   'numTweets': Number of tweets to recover
   'since': Initial date to recover tweets, Ex. "2017-03-23"
   'until': Final date to recover tweets, Ex. "2017-03-23"
   'lang': Language of the tweets, Ex. "es"
  '''

  numSearchs = numTweets / 100
  firstSearchCount = 100
  lastSearchCount = 100
  if numSearchs <= 0:
    # Less than 100 tweets
    firstSearchCount = numTweets
  else:
    # More than 100 tweets
    lastSearchCount = numTweets % 100

  numSearchs += 1
  numSearchs = int(numSearchs)

  totalTweets = None

  for j in range(numSearchs):
    try:
      if (j == 0):
        # First search
        print("First Search, recovering " +
              str(firstSearchCount) + " tweets")

        tweetsPrev = api.search(searchQuery, count=firstSearchCount, since=since,
                                until=until, lang=lang)

        totalTweets = tweetsPrev[:]

      elif j == (numSearchs - 1):
        if lastSearchCount > 0:
          # Check if there are some tweet prev or there aren't more tweets to
          # recover
          if(len(tweetsPrev) <= 0):
            break
          prevTweetID = tweetsPrev[-1].id - 1

          print("Last Search, recovering last " +
                str(lastSearchCount) + " tweets")
          tweets = api.search(searchQuery, count=lastSearchCount, since=since,
                              until=until, lang=lang, max_id=prevTweetID)
          totalTweets.extend(tweets)

      else:

          # Check if there are some tweet prev or there aren't more tweets to
          # recover
        if(len(tweetsPrev) <= 0):
          break
        prevTweetID = tweetsPrev[-1].id - 1
        print("Another Search, recovering another 100 tweets")
        tweets = api.search(searchQuery, count=100, since=since,
                            until=until, lang=lang, max_id=prevTweetID)
        tweetsPrev = tweets
        totalTweets.extend(tweets)

    except tweepy.TweepError as e:
      print ("\n\nA exception happenned while downloading tweets, this maybe because of the Twitter API rate limit (18000 tweets each 15 minutes).")
      print("\nException message: " + str(e))

      print("\nThis program is going to sleep for 5 min before retrying to download more tweets.\n\nPLEASE BE PATIENT AND WAIT.")
      j -= 1
      time.sleep(300)    # pause 5 minutes

  print("Total tweets recovered: " + str(len(totalTweets)))

  return totalTweets


def printTweetFields(tweet):
  print("\n\nTweet id: " + str(tweet.id))
  print("Tweet user: " + str(tweet.user.screen_name))
  print("Tweet text: " + str(tweet.text))
  print("Tweet user.followers: " + str(tweet.user.followers_count))
  print("Tweet user.following: " + str(tweet.user.friends_count))
  print("Tweet user.tweets: " + str(tweet.user.statuses_count))
  print("Tweet user.favourites: " + str(tweet.user.favourites_count))
  print("Tweet user.Timezone: " + str(tweet.user.time_zone))
  print("Tweet user.Location: " + str(tweet.user.location))
  print("Tweet entities: " + str(tweet.entities))


def saveTweetDetails(fileName, tweet):
  output = open(filename, 'w')
  output.write(str(tweet))
  output.flush()
  output.close()


def saveTweetsToCSV(tweets, csvFileName):
  '''
    Save the tweets and data about the users that wrote them
  '''

  csvFile = open(csvFileName, 'w', newline='')
  csvWriter = csv.writer(csvFile, delimiter=',')

  csvWriter.writerow(['ID', 'User', 'Created_at', 'Tweet', 'Following',
                      'Followers', 'Tweets_count', 'Favourites', 'Time_Zone', 'Location'])
  for tweet in tweets:
    csvWriter.writerow([tweet.id, tweet.user.screen_name, tweet.created_at, tweet.text, tweet.user.friends_count,
                        tweet.user.followers_count, tweet.user.statuses_count, tweet.user.favourites_count, tweet.user.time_zone, tweet.user.location])
  csvFile.close()
  return


def saveTweetsUsersToCSV(tweets, csvFileName):
  '''
    Save the users that wrote the revored tweets, do almost the same as saveTweetsToCSV method but using a set to remove duplicated users
  '''

  csvFile = open(csvFileName, 'w', newline='')
  csvWriter = csv.writer(csvFile, delimiter=',')

  csvWriter.writerow(['ID', 'Label', 'Following',
                      'Followers', 'Tweets_count', 'Favourites', 'Time_Zone', 'Location'])
  screenNameSet = set()
  for tweet in tweets:
    if tweet.user.screen_name not in screenNameSet:
      screenNameSet.add(tweet.user.screen_name)
      csvWriter.writerow([tweet.user.screen_name, tweet.user.screen_name, tweet.user.friends_count,
                          tweet.user.followers_count, tweet.user.statuses_count, tweet.user.favourites_count, tweet.user.time_zone, tweet.user.location])
  csvFile.close()
  return


def saveTweetRelationshipsToCSV(tweets, csvFileName):
  '''
    Save the relationships between tweets (Retweets and mentions)
  '''
  csvFile = open(csvFileName, 'w', newline='')
  csvWriter = csv.writer(csvFile, delimiter=',')
  csvWriter.writerow(['Source', 'Target'])

  # Count errors due to bad JSON parsing, these error might be for using the
  # "'" character in this field
  exceptionCounter = 0
  correctCounter = 0
  for tweet in tweets:
    jsonEntities = str(tweet.entities).replace('\'', '\"')
    try:
      entitiesJson = json.loads(jsonEntities)
    except Exception as e:
      exceptionCounter += 1
    finally:
      pass

    # If there is mentions (RT + Mentions) write it to the csv
    if len(entitiesJson['user_mentions']) > 0:
      for i in range(len(entitiesJson['user_mentions'])):
        correctCounter += 1
        csvWriter.writerow([tweet.user.screen_name, entitiesJson[
                           'user_mentions'][i]['screen_name']])

  print("Number of relationships lost due to errors: " +
        str(exceptionCounter) + "/" + str(correctCounter))

  csvFile.close()
  return


if __name__ == '__main__':
  # Main
  api = connectTwitterAPI()
  printsMenu()
