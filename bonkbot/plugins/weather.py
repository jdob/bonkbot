#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from xml.dom import minidom
import urllib

from bonkbot.bot.decorators import command


WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

WEATHER_FORMAT = 'Yahoo! Weather for %s, %s'
CURRENT_FORMAT = 'Current -> Temp: %sF, Condition: %s'
FORECAST_FORMAT = '%s -> Low: %sF, High: %sF, Condition: %s'


def init_plugin(config, irc_client):
    return [weather]


@command('weather')
def weather(message):
    """weather [zip] - Display weather information for [zip]."""

    args = message.command_args('weather')

    if len(args) > 0:
        zip_code = args[0]
        msgs = _weather_as_strings(zip_code)
        for m in msgs:
            message.reply(m)


def _weather_as_strings(zip_code):
    url = WEATHER_URL % zip_code
    dom = minidom.parse(urllib.urlopen(url))
    
    location_node = dom.getElementsByTagNameNS(WEATHER_NS, 'location')[0]
    location = WEATHER_FORMAT % (location_node.getAttribute('city'), location_node.getAttribute('region'))

    condition_node = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    conditions = CURRENT_FORMAT % (condition_node.getAttribute("temp"), condition_node.getAttribute('text'))

    weather = [location, conditions]

    forecast_nodes = dom.getElementsByTagNameNS(WEATHER_NS, 'forecast')
    for node in forecast_nodes:
        forecast = FORECAST_FORMAT % (node.getAttribute('day'), node.getAttribute('low'), node.getAttribute('high'), node.getAttribute('text'))
        weather.append(forecast)
        
    return weather
