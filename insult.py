from config import *
from irc_utils import *
import random

INSULTS = (
'Noob.',
'Anyone who told you to be yourself couldn\'t have given you worse advice.',
'Do you ever wonder what life would be like if you\'d had enough oxygen at birth?',
'Do you still love nature, despite what it did to you?',
'As an outsider, what do you think of the human race?',
'Have you considered suing your brains for non-support?',
'Every person has the right to be ugly, but you abused the privilege.',
'Go ahead, tell us everything you know. It\'ll only take 10 seconds.',
'I bet your brain feels as good as new, seeing that you\'ve never used it.',
'I thought of you all day today. I was at the zoo.',
'I\'m busy now. Can I ignore you some other time?',
'If ignorance is bliss, you must be the happiest person alive.',
'Keep talking, someday you\'ll say something intelligent.',
'So, a thought crossed your mind? Must have been a long and lonely journey.',
'I\'d like to help you out. Which way did you come in?',
'If I agreed with you we\'d both be wrong.',
'I\'ll try being nicer if you\'ll try being smarter.',
'I\'d insult you, but you\'re not bright enough to notice.',
)

def insult(irc, data):
    if data.find('!%s insult' % NICK) != -1:
        args = data.split()

        # Make sure a user was selected to be insulted
        if len(args) > args.index('insult') + 1:
            channel = args[2]
            user = args[args.index('insult') + 1]

            if user == NICK:
                msg(irc, channel, 'Nice try ' + author(data))
            else:
                insult = __randomInsult()
                msg(irc, channel, user + ' - ' + insult)

def __randomInsult():
    index = random.randint(0, len(INSULTS) - 1)
    return INSULTS[index]
