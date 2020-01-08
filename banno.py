import os
import requests
import json
import time
import asyncio
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
  "top_domains": []
  }

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
      # global stats
      # stats["total_tweets"]+=1
      process_tweet(json.loads(response_line))

def process_tweet(tweet):
  global stats, start_time

  stats["total_tweets"]+=1
  time_elapsed = time.time() - start_time

  stats["avg_per_sec"] = stats["total_tweets"]/(time.time()-launch_time)
  stats["avg_per_min"] = stats["avg_per_sec"]*60
  stats["avg_per_hr"] = stats["avg_per_min"]*60

  if time_elapsed >= log_interval:
    log_to_console(stats)
    start_time = time.time()

def log_to_console(stats):
  os.system('clear')
  pprint(stats)
  

bearer_token = BearerTokenAuth(consumer_key, consumer_secret)

# Listen to the stream. This reconnection logic will attempt to reconnect as soon as a disconnection is detected.
while True:
  asyncio.run(stream_connect(bearer_token))