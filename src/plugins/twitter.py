#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from bonkbot.decorators import command
import urllib
from xml.dom import minidom


def init_plugin(config, irc_client):
    return [twitter]

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
