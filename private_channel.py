from decorators import command

@command('invite')
def invite(message):
    '''invite [channel_name] [user] [user] ...'''

    args = message.command_args('invite')

    channel = args[0]
    invitees = args[1:]
    topic = '%s channel created by %s' % (message.config['name'], message.author())

    message.irc.send('JOIN %s\r\n' % channel)
    message.irc.send('TOPIC %s :%s\r\n' % (channel, topic))

    for person in invitees:
        message.irc.send('INVITE %s %s\r\n' % (person, channel))
