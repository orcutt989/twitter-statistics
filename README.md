# banno
 An application that connects to the Tweets API and processes incoming tweets to compute various statistics.

1. Install Ruby
2. Install jq a JSON parser
3. Install bundler `gem install bundler`
4. `cd` to project root
5. `bundle install` to install ruby gems
6. Authorize twurl with your app's consumer API key and secret key.

```bash
twurl authorize --consumer-key YOURKEY --consumer-secret YOURSECRET
```

7. Authorize the app from the resulting URL the previous command supplies and copy and paste the PIN from the browser to the console to authorize twurl.
