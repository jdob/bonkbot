
def speak(message):
    if not message.command('speak'):
        return

    cmd_args = message.command_args('speak')
    channel = cmd_args[0]
    speak_args = cmd_args[1:]
    say_this = ' '.join(speak_args)

    message.say(channel, say_this)
