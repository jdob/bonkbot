from config import *
from irc_utils import *
from xml.dom import minidom
import urllib

def hudson(irc, data):
    '''hudson [project] - Display the results of the last build for [project].'''

    if command(data, 'hudson'):
        args = data.split()

        if len(args) > args.index('hudson') + 1:
            project = args[args.index('hudson') + 1]

            status = __load(project)

            if status is not None:
                msg(irc, data, status)
        else:
            msg(irc, data, 'Please select a project from: ' + HUDSON_BUILDS.keys())

def __load(project):
    url = HUDSON_BUILDS[project]

    if url is not None:
        dom = minidom.parse(urllib.urlopen(url))
        return dom.getElementsByTagName('entry')[0].getElementsByTagName('title')[0].childNodes[0].data

    return None

if __name__ == "__main__":
    print(__load('content'))
