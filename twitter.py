from irc_utils import *
from xml.dom import minidom
import urllib

def twitter(irc, config, data):
    '''twitter [user] - Display the last tweet by twitter user [user].'''

    if command(config, data, 'twitter'):
        args = data.split()

        if len(args) > args.index('twitter') + 1:
            user = args[args.index('twitter') + 1]

            tweet = __findTweet(user)

            if tweet is not None:
                msg(irc, config, data, tweet)

def __findTweet(user):
    url = 'http://twitter.com/statuses/user_timeline.rss?screen_name=%s' % user
    dom = minidom.parse(urllib.urlopen(url))
    tweets = dom.getElementsByTagName('item')

    if len(tweets) > 0:
        latest = tweets.item(0).getElementsByTagName('title')[0].childNodes[0].data
        latest = latest.encode('UTF-8') # Needed since a coworker regularly tweets in German  :)
        return latest
    else:
        return None
