
def speak(message):
    if not message.command('speak'):
        return

    args = message.data.split()
    if len(args) > args.index('speak') + 1:
        channel = args[args.index('speak') + 1]

    speak_args = args[args.index('speak') + 2:]
    say_this = ' '.join(speak_args)

    message.say(channel, say_this)
