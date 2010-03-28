def give(message):
    if message.data.find('JOIN') != -1:
        newOp = message.author()
        if newOp != message.config['nick']:
            message.irc.send('MODE ' + message.channel()[1:] + ' +o ' + message.author() + '\r\n')
