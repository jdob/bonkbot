import pickle
import os

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
    for s in message.data.split():
        index = s.find('++')
        if index > 0:
            name = s[:index]

            if name[0] == ':':
                name = name[1:]

            if KARMA.has_key(name):
                KARMA[name] = int(KARMA[name]) + 1
            else:
                KARMA[name] = 1
            __printKarma(message, name)

def __remove(message):
    for s in message.data.split():
        index = s.find('--')
        if index > 0:
            name = s[:index]

            if name[0] == ':':
                name = name[1:]

            if KARMA.has_key(name):
                KARMA[name] = int(KARMA[name]) - 1
            else:
                KARMA[name] = -1
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
