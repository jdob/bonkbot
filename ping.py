from irc_utils import *
import os

def ping(irc, config, data):
    ''' ping [server] - Pings the given server. '''

    if command(config, data, 'ping'):
        args = data.split()

        if len(args) > args.index('ping') + 1:
            dest = args[args.index('ping') + 1]
            result = __doPing(dest)
            msg(irc, config, data, str(result))

def __doPing(dest):
    result = os.popen('ping %s -c 1' % dest)
    result.readline() # Throw away PING line
    return result.readline()

if __name__ == '__main__':
    result = __doPing('192.168.0.1')
    print 'Result: ' + result
