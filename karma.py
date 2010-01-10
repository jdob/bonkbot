from config import *
import pickle
import os

KARMA = {}

loaded = False

def karma(irc, data):

    global loaded
    if not loaded:
        load(KARMA_FILE)
        loaded = True

    if data.find('++') != -1:
        add(irc, data)

    if data.find('--') != -1:
        remove(irc, data)

    if data.find('!%s karma' % NICK) != -1:
        list(irc, data)

    save(KARMA_FILE)

def add(irc, data):
    channel = data.split()[2]
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
            printKarma(irc, channel, name)

def remove(irc, data):
    channel = data.split()[2]
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
            printKarma(irc, channel, name)

def list(irc, data):
    channel = data.split()[2]

    if len(KARMA) == 0:
        irc.send('PRIVMSG ' + channel + ' :I don\'t have any karma listings, you should make one.\r\n')
        return

    for user in KARMA:
        printKarma(irc, channel, user)

def save(filename):
    file = open(filename, 'wb')
    pickle.dump(KARMA, file)
    file.close()

def load(filename):
    global KARMA

    if os.path.exists(KARMA_FILE):
        file = open(filename, 'rb')
        KARMA = pickle.load(file)
        file.close()

def printKarma(irc, channel, user):
    if irc is not None:
        irc.send('PRIVMSG ' + channel + ' :' + user + ': ' + str(KARMA[user]) + '\r\n')


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
