from decorators import command
from xml.dom import minidom
import urllib

WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

WEATHER_FORMAT = 'Yahoo! Weather for %s, %s'
CURRENT_FORMAT = 'Current -> Temp: %sF, Condition: %s'
FORECAST_FORMAT = '%s -> Low: %sF, High: %sF, Condition: %s'

@command('weather')
def weather(message):
    '''weather [zip] - Display weather information for [zip].'''

    args = message.data.split()

    if len(args) > args.index('weather') + 1:
        zip_code = args[args.index('weather') + 1]
        msgs = __weather_as_strings(zip_code)
        for m in msgs:
            message.reply(m)

def __weather_as_strings(zip_code):
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

if __name__ == '__main__':
    print(weatherAsString('08056'))
