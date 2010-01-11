from config import *
from xml.dom import minidom
import urllib

def twitter(irc, data):
    if data.find('!%s twitter' % NICK) != -1:
        args = data.split()

        if len(args) > args.index('twitter') + 1:
            channel = args[2]
            user = args[args.index('twitter') + 1]
            url = 'http://twitter.com/statuses/user_timeline.rss?screen_name=%s' % user
            dom = minidom.parse(urllib.urlopen(url))
            tweets = dom.getElementsByTagName('item')

            if len(tweets) > 0:
                latest = tweets.item(0).getElementsByTagName('title')[0].childNodes[0].data
                latest = latest.encode('UTF-8') # Needed since a coworker regularly tweets in German  :)
                irc.send('PRIVMSG ' + channel + ' :"' + latest + '"\r\n')
