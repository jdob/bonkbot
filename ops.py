from config import *
from irc_utils import *

def give(irc, data):
    if data.find('JOIN') != -1:
        newOp = author(data)
        if newOp != NICK:
            irc.send('MODE ' + channel(data)[1:] + ' +o ' + author(data) + '\r\n')
