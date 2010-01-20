from irc_utils import *
import urllib

def quote(irc, config, data):
    '''quote [symbol] - Display information for the stock [symbol].'''

    if command(config, data, 'quote'):
        args = data.split()

        if len(args) > args.index('quote') + 1:
            symbol = args[args.index('quote') + 1]

            price = __lookup(symbol, 'l1')
            change = __lookup(symbol, 'c1')

            msg(irc, config, data, symbol + ' - Price: $' + price + ', Change: $' + change)

def __lookup(symbol, f):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, f)
    value = urllib.urlopen(url).read().strip().strip('"')
    return value
