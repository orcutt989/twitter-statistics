import os, requests, json, time, asyncio, emoji, re, requests_async, sys
from urllib.parse import urlparse
from collections import Counter
from pprint import pprint
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

consumer_key = os.environ.get('KEY','1')
consumer_secret = os.environ.get('SECRET','1')

log_interval=2.0
launch_time = start_time = time.time()

# Initialize global variables
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
num_tweets_with_images=0

# Sample stream url
# From https://developer.twitter.com/en/docs/labs/sampled-stream/quick-start
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

    if response.status_code != 200:
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
      await process_tweet(json.loads(response_line))

async def process_tweet(tweet):
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
  
  global num_tweets_with_urls, num_tweets_with_images
  urls_in_tweet=0
  contains_img_url=False
  try:
    urls_in_tweet, contains_img_url = find_urls(tweet)
  except:
    pass

  if urls_in_tweet > 0:
    num_tweets_with_urls+=1
  if contains_img_url:
    num_tweets_with_images+=1

  stats["perc_img"]=(num_tweets_with_images/stats["total_tweets"])*100
  stats["top_domains"]=Counter(domains).most_common(5)
  stats["perc_url"]=(num_tweets_with_urls/stats["total_tweets"])*100

  if time_elapsed >= log_interval:
    log_to_console(stats)
    start_time = time.time()

def log_to_console(stats):
  os.system('clear')
  pprint(stats)

def find_urls(tweet):
  urls_in_tweet=0
  images_in_tweet=0

  # Not all tweets have urls
  try:
    for url in tweet['data']['entities']['urls']:
      if urlparse(url['expanded_url']).netloc not in domains:
        domains[urlparse(url['expanded_url']).netloc]=1
        urls_in_tweet+=1
      else:
        domains[urlparse(url['expanded_url']).netloc]+=1 
      contains_img_url=has_image(url['expanded_url'])
  except:
    pass
  return urls_in_tweet, contains_img_url

# Surprisingly not very common
def has_image(url):
  return re.match("\.(jpeg|jpg|gif|png)$",url)
   
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
if len(sys.argv)>1 and sys.argv[1]=='-run':
  while True:
    asyncio.run(stream_connect(bearer_token))