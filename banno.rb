require 'typhoeus'
require 'base64'
require 'json'

@consumer_key = "" # Add your API key here
@consumer_secret = "" # Add your API secret key here

@bearer_token_url = "https://api.twitter.com/oauth2/token"
@stream_url = "https://api.twitter.com/labs/1/tweets/stream/sample"

def bearer_token
  return @bearer_token unless @bearer_token.nil?

  @credentials = Base64.encode64("#{@consumer_key}:#{@consumer_secret}").gsub("\n", "")
  
  @options = {
    body: {
      grant_type: "client_credentials"
    },
    headers: {
      "Authorization": "Basic #{@credentials}",
      "User-Agent": "TwitterDevSampledStreamQuickStartRuby",
    },
  }

  @response = Typhoeus.post(@bearer_token_url, @options)
  @body = JSON.parse(@response.body)
  @bearer_token = @body["access_token"] ||= nil
end

def stream_connect
  @options = {
    timeout: 20,
    method: 'get',
    headers: {
      "User-Agent": "TwitterDevSampledStreamQuickStartRuby",
      "Authorization": "Bearer #{bearer_token}",
    },
    params: {
      format: 'compact',
    },
  }

  @request = Typhoeus::Request.new(@stream_url, @options)
  @request.on_body do |chunk|
    puts chunk
  end
  @request.run
end

# Listen to the stream.
# This reconnection logic will attempt to reconnect when a disconnection is detected.
# To avoid rate limites, this logic implements exponential backoff, so the wait time
# will increase if the client cannot reconnect to the stream.
timeout = 0
while true
  stream_connect
  sleep 2 ** timeout
  timeout += 1
end