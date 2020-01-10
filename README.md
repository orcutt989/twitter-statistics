# banno

 An application that connects to the Tweets API and processes incoming tweets to compute various statistics.

## Requirements

1. An approved [Twitter dev account](https://developer.twitter.com/en/apply)
2. An existing Twitter developer app in your account's [Twitter app dashboard](https://developer.twitter.com/en/apps)

## Docker

1. Install Docker.
2. Get your consumer key and consumer secret from the [Twitter App Dashboard](https://developer.twitter.com/en/apps). (Details>>Keys and tokens).
3. Store your Twitter consumer key as a local environment variable named `KEY`.

   `export KEY='YOUR_CONSUMER_API_KEY'`

4. Store your Twitter consumer secret as a local environment variable named `SECRET`.

   `export SECRET='YOUR_CONSUMER_API_SECRET'`
5. Clone this repo.
6. `cd` to the directory of the project.
7. Run `docker-compose run banno`.

## No Docker

1. Install Python 3.7.4
1. Get your app's consumer key and consumer secret from the [Twitter App Dashboard](https://developer.twitter.com/en/apps). (Details>>Keys and tokens).
3. Store your Twitter consumer key as a local environment variable named `KEY`.

   `export KEY='YOUR_CONSUMER_API_KEY'`

4. Store your Twitter consumer secret as a local environment variable named `SECRET`.

   `export SECRET='YOUR_CONSUMER_API_SECRET'`
4. Clone this repo.
5. `cd` to the directory of the project.
6. Run `pip install requests emoji requests_async`.
7. Execute the Python script with `python banno.py` and watch the console.

![screenshot](screenshot.gif)

## Interesting Things

1. There aren't many tweets containing direct URLs to image files these days.
2. Async is processing is performed via [requests_async](https://github.com/encode/requests-async#streaming-responses--requests) and [asyncio](https://docs.python.org/3/library/asyncio.html)

## Todos

1. Better Logging
1. Interface with front-end like Splunk or Kibana
2. Better async
3. Testing, including async tests
