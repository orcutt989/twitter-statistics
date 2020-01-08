import os
import requests
import json
import time
import asyncio
import emoji
import re
from urllib.parse import urlparse
from collections import Counter
from reprint import output
import datetime as dt
from pprint import pprint
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
import requests_async

consumer_key = os.environ['KEY']
consumer_secret = os.environ['SECRET']

log_interval=2.0
launch_time = start_time = time.time()

stats = {
  "total_tweets": 0,
  "avg_per_sec": 0,
  "avg_per_min": 0,
  "avg_per_hr": 0,
  "perc_emoji": 0,
  "top_hashtags": [],
  "perc_url": 0,
  "perc_img": 0,
  "top_domains": [],
  "top_emoji": []
  }

emojis={}
hashtags={}
domains={}

num_tweets_with_emojis=0
num_tweets_with_urls=0

stream_url = "https://api.twitter.com/labs/1/tweets/stream/sample"

# Gets a bearer token
class BearerTokenAuth(AuthBase):
  def __init__(self, consumer_key, consumer_secret):
    self.bearer_token_url = "https://api.twitter.com/oauth2/token"
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.bearer_token = self.get_bearer_token()

  def get_bearer_token(self):
    response = requests.post(
      self.bearer_token_url, 
      auth=(self.consumer_key, self.consumer_secret),
      data={'grant_type': 'client_credentials'},
      headers={"User-Agent": "TwitterDevSampledStreamQuickStartPython"})

    if response.status_code is not 200:
      raise Exception(f"Cannot get a Bearer token (HTTP %d): %s" % (response.status_code, response.text))

    body = response.json()
    return body['access_token']

  def __call__(self, r):
    r.headers['Authorization'] = f"Bearer %s" % self.bearer_token
    return r

async def stream_connect(auth):
  response = await requests_async.get(stream_url, auth=auth, headers={"User-Agent": "TwitterDevSampledStreamQuickStartPython"}, stream=True)
  async for response_line in response.iter_lines():
    if response_line:
      process_tweet(json.loads(response_line))

def process_tweet(tweet):
  global stats, start_time

  stats["total_tweets"]+=1
  time_elapsed = time.time() - start_time
  stats["avg_per_sec"] = stats["total_tweets"]/(time.time()-launch_time)
  stats["avg_per_min"] = stats["avg_per_sec"]*60
  stats["avg_per_hr"] = stats["avg_per_min"]*60
  
  global num_tweets_with_emojis
  if has_emoji(tweet['data']['text']) > 0:
    num_tweets_with_emojis+=1

  stats["perc_emoji"] = (num_tweets_with_emojis/stats["total_tweets"])*100
  stats["top_emoji"] = Counter(emojis).most_common(5)
  get_hashtags(tweet)
  stats["top_hashtags"]=Counter(hashtags).most_common(5)
  
  global num_tweets_with_urls
  find_urls(tweet)
    
  stats["top_domains"]=Counter(domains).most_common(5)
  stats["perc_url"]=(num_tweets_with_urls/stats["total_tweets"])*100

  if time_elapsed >= log_interval:
    log_to_console(stats)
    start_time = time.time()

  #pprint(tweet['data']['text'])

def log_to_console(stats):
  os.system('clear')
  pprint(stats)

def find_urls(tweet):
  urls_in_tweet=0
  #urls=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet['data']['entities']['urls']['expanded_url'])
  try:
    for url in tweet['data']['entities']['urls']:
      if urlparse(url['expanded_url']).netloc not in domains:
        domains[urlparse(url['expanded_url']).netloc]=1
        urls_in_tweet+=1
        #pprint(urlparse(url['expanded_url']).netloc)
      else:
        domains[urlparse(url['expanded_url']).netloc]+=1
      #pprint(urlparse(url['expanded_url']).netloc)
  except:
    pass
  return urls_in_tweet


def get_hashtags(tweet):
  global hashtags
  for term in tweet['data']['text'].split():
    if term.startswith('#'):
      if not term in hashtags:
        hashtags[term]=1
      else:
        hashtags[term]+=1

def has_emoji(tweet):
  emojis_in_tweet=0
  for character in tweet:
    if character in emoji.UNICODE_EMOJI:
      emojis_in_tweet+=1
      global emojis
      if not character in emojis:
        emojis[character]=1
      else:
        emojis[character]+=1
  return emojis_in_tweet
  

bearer_token = BearerTokenAuth(consumer_key, consumer_secret)

# Listen to the stream. This reconnection logic will attempt to reconnect as soon as a disconnection is detected.
while True:
  asyncio.run(stream_connect(bearer_token))