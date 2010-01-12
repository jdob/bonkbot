from config import *
from irc_utils import msg

import irc_utils
import plugins
import socket
import sys
import traceback
import thread

def listen(irc):
    ''' Begins a loop to handle all incoming data from the IRC server. '''

    while True:
        data = irc.recv(4096)

        if DEBUG and len(data) > 0:
            print(data.rstrip())

        # Built in functionality rather than a plugin
        if data.find('PING') != -1:
            irc.send('PONG ' + data.split()[1] + '\r\n')
        
        # Run all plugins, catching any errors some may throw and logging the crap out of them
        for p in plugins.MSG_PLUGINS:
            try:
                p(irc, data)
            except:
                print('Error from plugin ' + p.__name__, sys.exc_info()[0])
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, limit=2, file=sys.stdout)
                traceback.print_tb(exceptionTraceback, limit=1, file=sys.stdout)

        # Display plugin help
        if data.find('!%s help' % NICK) != -1:
            msg(irc, data, 'Greetings traveler. Commands are triggered by typing !, then my name, then the command and any arguments.')
            for p in plugins.MSG_PLUGINS:
                if p.__doc__ is not None:
                    msg(irc, data, '   ' + p.__doc__)

            msg(irc, data, 'Thank you for using this bot. We hope no bodily harm comes to you during your usage.')

        # Let any plugins finish before quitting from command
        if data.find('!%s quit' % NICK) != -1:
            irc.send('QUIT :Fine, I\'ll leave... \r\n')
            sys.exit()

def connect():
    ''' Creates and returns a connection to the IRC server, using properies imported from config. '''

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to %s on port %s..." % (HOST, PORT))

    irc.connect((HOST, PORT))

    print('Connected')
    print(irc.recv(4096))
    print('Received initial data')

    print('Sending initial configuration...')
    irc.send('NICK %s\r\n' % NICK)
    irc.send('USER %s 0 * :%s\r\n' %(NICK, NAME))
    join(irc, CHANNELS)

    print('Sent initial configuration:')
    print('  NICK: %s' % NICK)
    print('  USER: %s' % NAME)
    print('  JOIN: %s' % CHANNELS)

    return irc

def start():
    ''' Connects and starts a new thread listening to incoming server data. The connection
        to the IRC server is returned. '''

    irc = connect()
    thread.start_new_thread(listen, (irc,))
    return irc

def speak(irc, channel, message):
    ''' Sends the given message to a channel on the IRC server. '''

    irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

def join(irc, channel):
    ''' Joins the specified channel. '''

    irc_utils.join(irc, channel)

if __name__ == "__main__":
    irc = connect()
    listen(irc)
