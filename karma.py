from config import *
from irc_utils import *
import pickle
import os

KARMA = {}

loaded = False

def karma(irc, data):
    '''karma - Display all karma data known to the bot.'''

    global loaded
    if not loaded:
        __load(KARMA_FILE)
        loaded = True

    if data.find('++') != -1:
        __add(irc, data)

    if data.find('--') != -1:
        __remove(irc, data)

    if command(data, 'karma'):
        __list(irc, data)

    __save(KARMA_FILE)

def __add(irc, data):
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
            __printKarma(irc, data, name)

def __remove(irc, data):
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
            __printKarma(irc, data, name)

def __list(irc, data):
    if len(KARMA) == 0:
        msg(irc, data, 'I don\'t have any karma listings, you should make one.')
        return

    for user in KARMA:
        __printKarma(irc, data, user)

def __save(filename):
    file = open(filename, 'wb')
    pickle.dump(KARMA, file)
    file.close()

def __load(filename):
    global KARMA

    if os.path.exists(KARMA_FILE):
        file = open(filename, 'rb')
        KARMA = pickle.load(file)
        file.close()

def __printKarma(irc, data, user):
    if irc is not None:
        msg(irc, data, user + ': ' + str(KARMA[user]))

if __name__ == '__main__':

    print(KARMA)

    add(None, 'PRIVMSG #test :jdob++')
    add(None, 'PRIVMSG #test :jdob++ jdob++')

    print(KARMA)

    remove(None, 'PRIVMSG #test :jdob--')
    remove(None, 'PRIVMSG #test :jdob-- jdob-- jdob-- jdob--')
    remove(None, 'PRIVMSG #test :mdob--')

    print(KARMA)

    tmpFile = '/tmp/karma.tmp'
    save(tmpFile)

    KARMA = {}

    print(KARMA)

    load(tmpFile)

    print(KARMA)

    os.remove(tmpFile)
