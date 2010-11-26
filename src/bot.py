#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import logging
import irc
import plugins
import thread

LOG = logging.getLogger(__name__)

class BonkMessage:
    def __init__(self, irc_client, config, data):
        self.irc_client = irc_client
        self.config = config
        self.data = data

    def command(self, cmd):
        '''
        Returns True if this message represents the specified command sent to the bot.
        '''
        return self.data.find('!%s %s' % (self.config['nick'], cmd)) != -1

    def is_join(self):
        '''
        Returns True if this message represents a user joining a channel in which the
        bot is; False otherwise.
        '''
        return self.data.find('JOIN') != -1

    def command_args(self, cmd):
        '''
        Parses out and returns the arguments to the given command.
        '''
        args = self.data.split()
        cmd_args = args[args.index(cmd) + 1:]
        return cmd_args

    def reply(self, message):
        '''
        Sends the given message back to the originator (either the author in the case a
        private message was sent to the bot or the channel on which it was received).
        '''
        destination = self.channel()
        if destination == self.config['nick']:
            destination = self.author()

        self.irc_client.send(destination, message)

    def channel(self):
        '''
        Returns the channel on which the message was received.
        '''
        return self.data.split()[2]

    def author(self):
        '''
        Returns the author of the received message.
        '''
        return self.data[1 : self.data.index('!')]

    def admin(self):
        '''
        Returns True if the author of the received message is an admin; False otherwise.
        '''
        author = self.author()
        for admin in self.config['admins']:
            if admin == author:
                return True
        else:
            return False

class BonkBot:

    def __init__(self, config):
        self.config = config
        self.irc_client = None

    def connect(self):
        self.irc_client = irc.IRCClient()

        # Load the necessary values from the config
        host = self.config['host']
        port = int(self.config['port'])
        nick = self.config['nick']
        name = self.config['name']
        channels = self.config['channels']

        LOG.info('Connecting to [%s] on port [%s]' % (host, port))
        self.irc_client.connect(host, port, nick, name)
        LOG.info('Connected to [%s]' % host)

        for channel in channels:
            self.irc_client.join(channel)

        LOG.info('Sent initial configuration:')
        LOG.info('  NICK: %s' % nick)
        LOG.info('  USER: %s' % name)
        LOG.info('  JOIN: %s' % channels)

    def listen(self):

        while True:
            data = self.irc_client.receive()

            if data.find('PING') != -1:
                self.irc_client.raw('PONG ' + data.split()[1] + '\r\n')

            message = BonkMessage(self.irc_client, self.config, data)
            for p in plugins.MSG_PLUGINS:
                try:
                    thread.start_new_thread(p, (message,))
                except:
                    LOG.exception('Error from plugin [%s]' % p.__name__)

            if message.command('help'):
                message.reply('Greetings traveler. Commands are triggered by typing !, then my name, then the command and any arguments it may have.')

                for p in plugins.MSG_PLUGINS:
                    if p.__doc__ is not None and p.__doc__.strip() != '':
                        message.reply('   %s' % p.__doc__)

            if message.command('quit'):
                message.irc_client.quit('Fine, I\'ll leave...')

    def start(self):
        self.connect()
        self.listen()

    def startd(self):
        self.connect()
        thread.start_new_thread(self.listen, ())
