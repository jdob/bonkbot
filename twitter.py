from decorators import command
import urllib
from xml.dom import minidom

@command('twitter')
def twitter(message):
    '''twitter [user] - Display the last tweet by twitter user [user].'''

    args = message.data.split()

    if len(args) > args.index('twitter') + 1:
        user = args[args.index('twitter') + 1]
            
        tweet = __find_tweet(user)

        if tweet is not None:
            message.reply(tweet)

def __find_tweet(user):
    url = 'http://twitter.com/statuses/user_timeline.rss?screen_name=%s' % user
    dom = minidom.parse(urllib.urlopen(url))
    tweets = dom.getElementsByTagName('item')

    if len(tweets) > 0:
        latest = tweets.item(0).getElementsByTagName('title')[0].childNodes[0].data
        latest = latest.encode('UTF-8') # Needed since a coworker regularly tweets in German  :)
        return latest
    else:
        return None
