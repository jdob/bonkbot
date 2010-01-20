
def command(config, data, command):
    ''' Returns True or False depending on if the given command was issued to the bot. '''

    return data.find('!%s %s' % (config['nick'], command)) != -1

def msg(irc, config, data, message):
    ''' Sends a message back to the appropriate destination, either a private message or a channel,
        based on what is found in the data. '''
    
    destination = channel(data)
    if destination == config['nick']:
        destination = author(data)

    irc.send('PRIVMSG ' + destination + ' :' + message + '\r\n')

def join(irc, channel):
    irc.send('JOIN %s\r\n' % channel)

def leave(irc, channel):
    irc.send('PART %s\r\n' % channel)

def channel(data):
    return data.split()[2]

def author(data):
    return data[1 : data.index('!')]

if __name__ == '__main__':
    print(author(':jdob!~jdob@127.0.0.1 MODE #bonk +o bonk'))
