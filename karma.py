from irc_utils import *
import pickle
import os

KARMA = {}

loaded = False

def karma(irc, config, data):
    '''karma - Display all karma data known to the bot.'''

    global loaded
    if not loaded:
        __load(config['karmaFile'])
        loaded = True

    if data.find('++') != -1:
        __add(irc, config, data)

    if data.find('--') != -1:
        __remove(irc, config, data)

    if command(config, data, 'karma'):
        __list(irc, config, data)

    __save(config['karmaFile'])

def __add(irc, config, data):
    for s in data.split():
        index = s.find('++')
        if index > 0:
            name = s[:index]

            if name[0] == ':':
                name = name[1:]

            if KARMA.has_key(name):
                KARMA[name] = int(KARMA[name]) + 1
            else:
                KARMA[name] = 1
            __printKarma(irc, config, data, name)

def __remove(irc, config, data):
    for s in data.split():
        index = s.find('--')
        if index > 0:
            name = s[:index]

            if name[0] == ':':
                name = name[1:]

            if KARMA.has_key(name):
                KARMA[name] = int(KARMA[name]) - 1
            else:
                KARMA[name] = -1
            __printKarma(irc, config, data, name)

def __list(irc, config, data):
    if len(KARMA) == 0:
        msg(irc, config, data, 'I don\'t have any karma listings, you should make one.')
        return

    for user in KARMA:
        __printKarma(irc, config, data, user)

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

def __printKarma(irc, config, data, user):
    if irc is not None:
        msg(irc, config, data, user + ': ' + str(KARMA[user]))

if __name__ == '__main__':

    print(KARMA)

    __add(None, 'PRIVMSG #test :jdob++')
    __add(None, 'PRIVMSG #test :jdob++ jdob++')

    print(KARMA)

    __remove(None, 'PRIVMSG #test :jdob--')
    __remove(None, 'PRIVMSG #test :jdob-- jdob-- jdob-- jdob--')
    __remove(None, 'PRIVMSG #test :mdob--')

    print(KARMA)

    tmpFile = '/tmp/karma.tmp'
    __save(tmpFile)

    KARMA = {}

    print(KARMA)

    __load(tmpFile)

    print(KARMA)

    os.remove(tmpFile)
