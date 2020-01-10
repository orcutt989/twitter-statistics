# banno

## This is a proof-of-concept

 An application that connects to the Tweets API and processes incoming tweets to compute various statistics.

## Docker

1. Install Docker
2. Clone this repo.
3. `cd` to the directory of the project
4. Run `docker-compose run banno`

## No Docker

1. Install Python 3.7.4
2. Store your Twitter consumer key as an environment variable named `KEY`.
3. Store your Twitter consumer secret as an environment variable named `SECRET`.
4. Clone this repo.
5. `cd` to the directory of the project
6. Execute the Python script with `python banno.py` and watch the console.

![screenshot](screenshot.gif)

## Interesting Things

1. There aren't many tweets containing direct URLs to image files these days.
2. Async is processing is performed via [requests_async](https://github.com/encode/requests-async#streaming-responses--requests) and [asyncio](https://docs.python.org/3/library/asyncio.html)

## Todos

1. Better Logging
1. Interface with front-end like Splunk or Kibana
2. Better async
3. Testing, including async tests
