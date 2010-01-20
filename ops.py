from irc_utils import *

def give(irc, config, data):
    if data.find('JOIN') != -1:
        newOp = author(data)
        if newOp != config['nick']:
            irc.send('MODE ' + channel(data)[1:] + ' +o ' + author(data) + '\r\n')
