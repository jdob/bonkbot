from decorators import command, admin

@command('speak')
@admin
def speak(message):
    cmd_args = message.command_args('speak')
    channel = cmd_args[0]
    speak_args = cmd_args[1:]
    say_this = ' '.join(speak_args)

    message.say(channel, say_this)

@command('join')
@admin
def join(message):
    cmd_args = message.command_args('join')
    channel = cmd_args[0]
    message.irc.send('JOIN %s\r\n' % channel)

@command('leave')
@admin
def leave(message):
    cmd_args = message.command_args('leave')
    channel = cmd_args[0]
    message.irc.send('PART %s\r\n' % channel)
