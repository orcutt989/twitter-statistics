# twitter-statistics

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
7. Execute the Python script with `python banno.py -run` and watch the console.

![screenshot](screenshot.gif)

## Interesting Things

1. There aren't many tweets containing direct URLs to image files these days.
2. Async processing is performed via [requests_async](https://github.com/encode/requests-async#streaming-responses--requests) and [asyncio](https://docs.python.org/3/library/asyncio.html)

## Culture

More important than tooling or automation is culture. You can use Kubernetes and CI/CD automation, but none of it will work without making decisions about your product's development process and team culture.

For this repository the decision was made that the development team would perform development on versioned branches instead of directly to master.  Releases are not entirely automatic, however when a PR for a development branch is approved and merged, a release is generated based on that version number.

## Automation Overview

All automations are handled by Github Actions.

* Continuous Integration
* Continuous Deployment
* Python Linting
* Integration Testing
* Automated Versioning
* Documentation Generation
* CHANGELOG Generation

## Releases

Draft releases are generated when a commit to master is detected, but publishing is still manual. This prevents any unintended features from entering the latest release.

## Branch Protection

Pushing directly to mater is prohibited by anyone.  A separate branch (a "development branch") needs to be created, and then a PR to merge a development branch into master will need to be reviewed.

## Continuous Integration

Continuous integration is performed by GitHub actions. To view the latest actions and whether they have passed or not click the `Actions` button at the top of the repo.

Tests are executed on every commit with `pytest` and are located in `test_banno.py`.

## Continuous Deployment & Automatic Versioning

When a PR is approved and the respective branch is merged a release is drafted and the version incremented. At this time versioning is minor only but can be changed depending on a keyword in a PR title.  At this time there are no Git Hub actions that support incrementing the version, drafting a release, and publshing a release. For the sake of time and without having to write our own Github Action, we'll say that releases need to be manually published to prevent mistakes from entering a public build.

## CHANGELOG generation

The Changelog is generated when a release is published. Changes include commits and PR titles if they are available.  Changes are also supplied to the body of the release upon draft.

## Linting

Python linting is also performed with GitHub actions and utilizes `Flake8`. Linting is performed on every commit.

## Integration Tests

For the sake of time a simple test suite of 2 tests were added to this repository. To satisfy real-word demands, the test suite would most likely be 500+ lines long for sufficient code coverage.

## Mutation Tests

`mutmut` reports 162 possible places for mutations not covered by tests. For the sake of time these were not added, however mutation tests would most likely expand the tests by anywhere from 200-500 more lines of code.  `mutmut` could be included in a GitHub Action, however it takes about 5 minutes for it to run all mutation tests and since there are no cases testing for these at this time, it was omitted and ran manually.

## Spell Check

At this time there is not a sufficient Git Hub action to implement a spell-checker. One will need to be written.  