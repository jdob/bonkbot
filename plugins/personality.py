#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import random

from bonkbot.bot.decorators import command


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

COMPLIMENTS = (
'Wow %s, how insightful.',
'That\'s a great idea %s, I wish I had thought of that.',
'That sounds good %s, is there a JIRA for it?'
)


def init_plugin(config, irc_client):
    return [insult, compliment]


@command('insult')
def insult(message):
    '''insult [user] - Send a random insult to [user].'''

    cmd_args = message.command_args('insult')

    # Make sure a user was selected to be insulted
    if len(cmd_args) > 0:
        user = cmd_args[0]

        if user == message.config['nick']:
            message.reply('Nice try ' + message.author())
        elif user in message.config['admins']:
            message.reply('I would never insult an admin!')
            message.reply(message.author() + ' - ' + __random(INSULTS))
        else:
            message.reply(user + ' - ' + __random(INSULTS))


def compliment(message):
    if random.randint(0, 1000) == 705:
        msg = __random_sub(COMPLIMENTS, message.author())
        message.reply(msg)


def __random(comments):
    index = random.randint(0, len(comments) - 1)
    return comments[index]


def __random_sub(comments, sub):
    index = random.randint(0, len(comments) - 1)
    return comments[index] % sub
