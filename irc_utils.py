def msg(irc, channel, message):
    irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

    
