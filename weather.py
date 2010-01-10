from config import *
from xml.dom import minidom
import urllib

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
WEATHER_FORMAT = '%s -> Temp: %sF, Condition: %s'

def weatherAsString(zipCode):
    url = WEATHER_URL % zipCode
    dom = minidom.parse(urllib.urlopen(url))
    condition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    
    return WEATHER_FORMAT % (dom.getElementsByTagName('title')[0].firstChild.data, condition.getAttribute("temp"), condition.getAttribute('text'))

def weather(irc, data):
    if data.find('!%s weather' % NICK) != -1:
        args = data.split()

        if len(args) > args.index('weather') + 1:
            channel = args[2]
            zipCode = args[args.index('weather') + 1]
            message = weatherAsString(zipCode)
            irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

if __name__ == '__main__':
    print(weatherAsString('08056'))
