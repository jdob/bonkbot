
def speak(message):
    if not message.command('speak'):
        return

    cmd_args = message.command_args('speak')
    channel = cmd_args[0]
    speak_args = cmd_args[1:]
    say_this = ' '.join(speak_args)

    message.say(channel, say_this)

def join(message):
    if not message.command('join'):
        return

    cmd_args = message.command_args('join')
    channel = cmd_args[0]
    message.irc.send('JOIN %s\r\n' % channel)

def leave(message):
    if not message.command('leave'):
        return

    cmd_args = message.command_args('leave')
    channel = cmd_args[0]
    message.irc.send('PART %s\r\n' % channel)
