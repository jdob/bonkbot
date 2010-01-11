def msg(irc, channel, message):
    irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

def author(data):
    return data[1 : data.index('!')]

if __name__ == '__main__':
    print(author(':jdob!~jdob@127.0.0.1 MODE #bonk +o bonk'))

