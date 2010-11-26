from decorators import command
import urllib

@command('stock')
def stock(message):
    '''quote [symbol] - Display information for the stock [symbol].'''

    args = message.data.split()

    if len(args) > args.index('stock') + 1:
        symbol = args[args.index('stock') + 1]

        price = __lookup(symbol, 'l1')
        change = __lookup(symbol, 'c1')

        message.reply(symbol + ' - Price: $' + price + ', Change: $' + change)

def __lookup(symbol, f):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, f)
    value = urllib.urlopen(url).read().strip().strip('"')
    return value
