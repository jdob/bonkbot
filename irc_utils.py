from config import *

def msg(irc, data, message):
    ''' Sends a message back to the appropriate destination, either a private message or a channel,
        based on what is found in the data. '''
    # For now, assume all messages go to channel; still need to add private message checks
    
    destination = channel(data)
    if destination == NICK:
        destination = author(data)

    irc.send('PRIVMSG ' + destination + ' :' + message + '\r\n')

def channel(data):
    return data.split()[2]

def author(data):
    return data[1 : data.index('!')]

if __name__ == '__main__':
    print(author(':jdob!~jdob@127.0.0.1 MODE #bonk +o bonk'))

