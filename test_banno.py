#test_banno.py

import pytest, banno

tweet = '''
{
  'data': {
    'id': '1220025596324892672',
    'created_at': '2020-01-22T16:49:03.000Z',
    'text': 'Tak menyesal aku tido lambat sebab tengok vid ni 😂😂 https://t.co/QNgkvTw7Ae',
    'author_id': '904377000474820608',
    'referenced_tweets': [{
      'type': 'quoted',
      'id': '1219633686460686336'
    }],
    'entities': {
      'urls': [{
        'start': 52,
        'end': 75,
        'url': 'https://t.co/QNgkvTw7Ae',
        'expanded_url': 'https://twitter.com/Payishahyin/status/1219633686460686336',
        'display_url': 'twitter.com/Payishahyin/st…'
      }]
    },
    'format': 'default'
  }
}
'''


tweet2 = '''
{
  'data': {
    'id': '1220027100821905409',
    'created_at': '2020-01-22T16:55:02.000Z',
    'text': 'RT @AbAmri: بمناسبة انعقاد #منتدى_الرياض_الاقتصادي\nلا بد أن نذكّر ونذكّر حضوره من رجال وسيدات الأعمال بمسؤوليتهم الوطنية تجاه شبابنا وبناتن…',
    'author_id': '2493022118',
    'referenced_tweets': [{
      'type': 'retweeted',
      'id': '1219722096844181506'
    }],
    'entities': {
      'hashtags': [{
        'start': 27,
        'end': 50,
        'tag': 'منتدى_الرياض_الاقتصادي'
      }],
      'mentions': [{
        'start': 3,
        'end': 10,
        'username': 'AbAmri'
      }]
    },
    'format': 'default'
  }
}
'''

def test_has_emoji_true():
  assert banno.has_emoji(tweet) > 0

def test_has_emoji_false():
  assert banno.has_emoji(tweet2) == 0