from config import *
from irc_utils import msg
import urllib

def quote(irc, data):
    if data.find('!%s quote' % NICK) != -1:
        args = data.split()

        if len(args) > args.index('quote') + 1:
            channel = args[2]
            symbol = args[args.index('quote') + 1]

            price = __lookup(symbol, 'l1')
            change = __lookup(symbol, 'c1')

            msg(irc, channel, symbol + ' - Price: $' + price + ', Change: $' + change)

def __lookup(symbol, f):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, f)
    value = urllib.urlopen(url).read().strip().strip('"')
    return value
