import pickle
import re
import os

VALID_NAME = r'^([A-Za-z0-9_-]|\[|\])*$'

KARMA = {}

loaded = False

def karma(message):
    '''karma - Display all karma data known to the bot.'''

    global loaded
    if not loaded:
        __load(message.config['karmaFile'])
        loaded = True

    if message.data.find('++') != -1:
        __add(message)

    if message.data.find('--') != -1:
        __remove(message)

    if message.command('karma'):
        __list(message)

    __save(message.config['karmaFile'])

def __add(message):
    __assign_karma(message, '++', 1)

def __remove(message):
    __assign_karma(message, '--', -1)

def __assign_karma(message, flag, step):
    for s in message.data.split():
        if not s.endswith(flag):
            continue

        name = s[0:len(s) - 2]
        
        if name[0] == ':':
            name = name[1:]

        if not re.match(VALID_NAME, name):
            print('Not a valid name [%s]' % name)
            continue

        if KARMA.has_key(name):
            KARMA[name] = int(KARMA[name]) + step
        else:
            KARMA[name] = step

        __printKarma(message, name)

def __list(message):
    if len(KARMA) == 0:
        message.reply('I don\'t have any karma listings, you should make one.')
        return

    for user in KARMA:
        __printKarma(message, user)

def __save(filename):
    file = open(filename, 'wb')
    pickle.dump(KARMA, file)
    file.close()

def __load(filename):
    global KARMA

    if os.path.exists(filename):
        file = open(filename, 'rb')
        KARMA = pickle.load(file)
        file.close()

def __printKarma(message, user):
    message.reply(user + ': ' + str(KARMA[user]))
