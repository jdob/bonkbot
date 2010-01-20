from irc_utils import *
from xml.dom import minidom
import urllib

def hudson(irc, config, data):
    '''hudson [project] - Display the results of the last build for [project].'''

    if command(config, data, 'hudson'):
        args = data.split()

        if len(args) > args.index('hudson') + 1:
            project = args[args.index('hudson') + 1]

            status = __load(config['hudsonUrl'], project)

            if status is not None:
                msg(irc, config, data, status)
        else:
            msg(irc, config, data, 'Please select a project from: ' + ', '.join(config['hudsonBuilds']))

def __load(url, project):

    if url is not None:
        url = url % project
        dom = minidom.parse(urllib.urlopen(url))
        status = dom.getElementsByTagName('entry')[0].getElementsByTagName('title')[0].childNodes[0].data
        link = dom.getElementsByTagName('entry')[0].getElementsByTagName('link')[0].getAttribute('href')
        return status + ' -- ' + link

    return None

if __name__ == "__main__":
    print(__load('content'))
