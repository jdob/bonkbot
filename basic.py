from config import *

def echo(irc, data):
    if data.find('!%s echo' % NICK) != -1:
        if len(data.split()) > 5:
            irc.send('PRIVMSG #test :ECHO ' + ' '.join(data.split()[5:]) + '\r\n')

def log(irc, data):
    if len(data) > 0:
        print(data.rstrip())
