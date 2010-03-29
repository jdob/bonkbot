from decorators import command
from xml.dom import minidom
import urllib

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
WEATHER_FORMAT = '%s -> Temp: %sF, Condition: %s'

@command('weather')
def weather(message):
    '''weather [zip] - Display weather information for [zip].'''

    args = message.data.split()

    if len(args) > args.index('weather') + 1:
        zipCode = args[args.index('weather') + 1]
        message.reply(__weather_as_string(zipCode))

def __weather_as_string(zipCode):
    url = WEATHER_URL % zipCode
    dom = minidom.parse(urllib.urlopen(url))
    condition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    
    return WEATHER_FORMAT % (dom.getElementsByTagName('title')[0].firstChild.data, condition.getAttribute("temp"), condition.getAttribute('text'))

if __name__ == '__main__':
    print(weatherAsString('08056'))
