#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import urllib

from bonkbot.bot.decorators import command


def init_plugin(config, irc_client):
    return [stock]


@command('stock')
def stock(message):
    """quote [symbol] - Display information for the stock [symbol]."""

    args = message.data.split()

    if len(args) > args.index('stock') + 1:
        symbol = args[args.index('stock') + 1]

        price = _lookup(symbol, 'l1')
        change = _lookup(symbol, 'c1')

        message.reply(symbol + ' - Price: $' + price + ', Change: $' + change)


def _lookup(symbol, f):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, f)
    value = urllib.urlopen(url).read().strip().strip('"')
    return value
