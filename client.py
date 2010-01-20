from irc_utils import msg

import irc_utils
import plugins
import socket
import sys
import traceback
import thread
import simplejson

config = ''

def listen(irc):
    ''' Begins a loop to handle all incoming data from the IRC server. '''

    global config
    debug = bool(config['debug'])

    while True:
        data = irc.recv(4096)

        if debug and len(data) > 0:
            print(data.rstrip())

        # Built in functionality rather than a plugin
        if data.find('PING') != -1:
            irc.send('PONG ' + data.split()[1] + '\r\n')
        
        # Run all plugins, catching any errors some may throw and logging the crap out of them
        for p in plugins.MSG_PLUGINS:
            try:
                p(irc, config, data)
            except:
                print('Error from plugin ' + p.__name__, sys.exc_info()[0])
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, limit=2, file=sys.stdout)
                traceback.print_tb(exceptionTraceback, limit=1, file=sys.stdout)

        # Display plugin help
        if data.find('!%s help' % config['nick']) != -1:
            msg(irc, config, data, 'Greetings traveler. Commands are triggered by typing !, then my name, then the command and any arguments.')
            for p in plugins.MSG_PLUGINS:
                if p.__doc__ is not None:
                    msg(irc, config, data, '   ' + p.__doc__)

            msg(irc, config, data, 'Thank you for using this bot. We hope no bodily harm comes to you during your usage.')

        # Let any plugins finish before quitting from command
        if data.find('!%s quit' % config['nick']) != -1:
            irc.send('QUIT :Fine, I\'ll leave... \r\n')
            sys.exit()

def connect():
    ''' Creates and returns a connection to the IRC server, using properies imported from config. '''
    global config
    config = simplejson.load(file('config.json'))

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = config['host']
    port = int(config['port'])
    nick = config['nick']
    name = config['name']
    channels = config['channels']

    print("Connecting to %s on port %s..." % (host, port))

    irc.connect((host, port))

    print('Connected')
    print(irc.recv(4096))
    print('Received initial data')

    print('Sending initial configuration...')
    irc.send('NICK %s\r\n' % nick)
    irc.send('USER %s 0 * :%s\r\n' % (nick, name))
    join(irc, channels)

    print('Sent initial configuration:')
    print('  NICK: %s' % nick)
    print('  USER: %s' % name)
    print('  JOIN: %s' % channels)

    return irc

def configure():
    ''' Loads the latest configuration from the disk. '''
    global config
    config = simplejson.load(file('config.json'))

def speak(irc, channel, message):
    ''' Sends the given message to a channel on the IRC server. '''

    irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

def join(irc, channel):
    ''' Joins the specified channel. '''

    irc_utils.join(irc, channel)

def leave(irc, channel):
    ''' Leaves the specified channel. '''

    irc_utils.leave(irc, channel)

def start():
    ''' Connects and starts a new thread listening to incoming server data. The connection
        to the IRC server is returned. '''

    configure()

    irc = connect()
    thread.start_new_thread(listen, (irc,))
    return irc

if __name__ == "__main__":
    configure()
    irc = connect()
    listen(irc)
