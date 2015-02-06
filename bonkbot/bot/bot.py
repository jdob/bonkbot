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
import thread

# -- constants ----------------------------------------------------------------

LOG = logging.getLogger(__name__)

# -- classes ------------------------------------------------------------------

class BonkMessage:
    '''
    Represents an inbound message to the bot; each instance of this class is
    a new message. Utility methods are provided for handling the message.
    '''

    def __init__(self, irc_client, config, data):
        self.irc_client = irc_client
        self.config = config
        self.data = data

    def command(self, cmd):
        '''
        Returns True if this message represents the specified command sent to the bot.
        '''
        return self.data.find('!%s %s' % (self.config.get('bot', 'nick'), cmd)) != -1

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
        if destination == self.config.get('bot', 'nick'):
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
        for admin in self.config.get('bot', 'admins').split(','):
            if admin == author:
                return True
        else:
            return False


class BonkBot:
    '''
    Represents an instance of the bot. The configuration specified at instantiation
    is used to drive basic bot behavior such as IRC server location, bot nickname,
    and location of plugin files.
    '''

    def __init__(self, config, plugin_loader):
        self.config = config
        self.plugin_loader = plugin_loader

        self.irc_client = None
        self.listeners = []

    def connect(self):
        self.irc_client = irc.IRCClient()

        # Load the necessary values from the config
        host = self.config.get('server', 'host')
        port = self.config.getint('server', 'port')
        nick = self.config.get('bot', 'nick')
        name = self.config.get('bot', 'name')
        channels = self.config.get('bot', 'channels').split(',')

        # Establish the connection to the chat server
        LOG.info('Connecting to [%s] on port [%s]' % (host, port))
        self.irc_client.connect(host, port, nick, name)
        LOG.info('Connected to [%s]' % host)

        # Join any channels configured by default
        for channel in channels:
            self.irc_client.join(channel)

        LOG.info('Sent initial configuration:')
        LOG.info('  NICK: %s' % nick)
        LOG.info('  USER: %s' % name)
        LOG.info('  JOIN: %s' % channels)

    def load_plugins(self):
        loaded_listeners = self.plugin_loader.load(self.irc_client)
        self.listeners += loaded_listeners
        
    def run(self):
        running = True
        while running:
            data = None
            try:
                data = self.irc_client.receive()
            except KeyboardInterrupt:
                self.irc_client.quit('Being kicked out now...')
                break

            if data.find('PING') != -1:
                self.irc_client.raw('PONG ' + data.split()[1] + '\r\n')

            message = BonkMessage(self.irc_client, self.config, data)
            for l in self.listeners:
                try:
                    thread.start_new_thread(self._notify_listener, (l, message))
                except Exception:
                    LOG.exception('Error launching thread to handle listener [%s]' % l.__name__)

            if message.command('help'):
                message.reply('Greetings traveler. Commands are triggered by typing !, then my name, then the command and any arguments it may have.')

                for l in self.listeners:
                    if l.__doc__ is not None and l.__doc__.strip() != '':
                        message.reply('   %s' % l.__doc__)

            if message.command('quit'):
                running = False
                self.irc_client.quit('Fine, I\'ll leave...')

    def start(self):
        self.connect()
        self.load_plugins()
        self.run()

    def startd(self):
        self.connect()
        thread.start_new_thread(self.run, ())

    def _notify_listener(self, listener_func, message):
        try:
            listener_func(message)
        except Exception:
            LOG.exception('Error from listener [%s]' % listener_func.__name__)
