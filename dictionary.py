from irc_utils import *
from xml.dom import minidom
import urllib

def wotd(irc, config, data):
    '''wotd - Display the dictionary.com word of the day.'''

    if command(config, data, 'wotd'):
        message = __load()
        msg(irc, config, data, 'Word of the Day: ' + message)

def __load():
    url = 'http://dictionary.reference.com/wordoftheday/wotd.rss'
    dom = minidom.parse(urllib.urlopen(url))
    desc = dom.getElementsByTagName('channel')[0].getElementsByTagName('item')[0].getElementsByTagName('description')[0].childNodes[0].data
    message = desc[:desc.index('<')]
    return message
