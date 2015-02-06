#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import pickle
import re
import os


VALID_NAME = r'^([A-Za-z0-9_-]|\[|\])*$'

CONFIG = None
KARMA = {}


def init_plugin(config, irc_client):
    global CONFIG
    CONFIG = config

    global KARMA
    filename = config.get('plugin', 'karma_file')
    if os.path.exists(filename):
        file = open(filename, 'rb')
        KARMA = pickle.load(file)
        file.close()

    return [karma]


def karma(message):
    """karma - Display all karma data known to the bot."""

    if message.data.find('++') != -1:
        _add(message)

    if message.data.find('--') != -1:
        _remove(message)

    if message.command('karma'):
        _list(message)

    _save(CONFIG.get('plugin', 'karma_file'))


def _add(message):
    _assign_karma(message, '++', 1)


def _remove(message):
    _assign_karma(message, '--', -1)


def _assign_karma(message, flag, step):
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

        _print_karma(message, name)


def _list(message):
    if len(KARMA) == 0:
        message.reply('I don\'t have any karma listings, you should add some.')
        return

    for user in KARMA:
        _print_karma(message, user)


def _save(filename):
    f = open(filename, 'wb')
    pickle.dump(KARMA, f)
    f.close()


def _print_karma(message, user):
    message.reply(user + ': ' + str(KARMA[user]))
