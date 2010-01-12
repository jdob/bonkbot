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

MAKER_COMMENTS = (
'I could never insult the maker %s',
'I would be nothing without %s.',
)

COMPLIMENTS = (
'Wow %s, how insightful.',
'That\'s a great idea %s, I wish I had thought of that.',
'That sounds good %s, is there a JIRA for it?'
)

MARIO = (
'I straight up just killed a dude with a turnip.',
'Where are they getting all these hammers?!',
'There are man eating plants in these pipes!'
)

def insult(irc, data):
    '''insult [user] - Send a random insult to [user].'''

    if data.find('!%s insult' % NICK) != -1:
        args = data.split()

        # Make sure a user was selected to be insulted
        if len(args) > args.index('insult') + 1:
            user = args[args.index('insult') + 1]

            if user == NICK:
                msg(irc, data, 'Nice try ' + author(data))
            elif user == MAKER:
                msg(irc, data, 'I would never insult the maker!')
                msg(irc, data, author(data) + ' - ' + __random(INSULTS))
            else:
                msg(irc, data, user + ' - ' + __random(INSULTS))

def maker(irc, data):
    '''maker - Speak random praise about the maker.'''

    if data.find('!%s maker' % NICK) != -1:
        msg(irc, data, __randomSub(MAKER_COMMENTS, MAKER))

def mario(irc, data):
    '''mario - Quotes from the great Super Mario.'''

    if data.find('!%s mario' % NICK) != -1:
        msg(irc, data, __random(MARIO))

def bacon(irc, data):
    if data.find('!%s bacon' % NICK) != -1:
        msg(irc, data, 'BACON!')

def compliment(irc, data):
    if random.randint(0, 1000) == 705:
        message = __randomSub(COMPLIMENTS, author(data))
        msg(irc, data, message)

def __random(list):
    index = random.randint(0, len(list) - 1)
    return list[index]

def __randomSub(list, sub):
    index = random.randint(0, len(list) - 1)
    return list[index] % sub
