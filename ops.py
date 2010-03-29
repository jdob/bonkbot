def give(message):
    if message.data.find('JOIN') != -1:
        new_op = message.author()

        # Don't try to op yourself
        if new_op != message.config['nick']:
            message.irc.send('MODE ' + message.channel()[1:] + ' +o ' + message.author() + '\r\n')
