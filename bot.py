
import logging
import plugins
import socket
import thread

LOG = logging.getLogger('bonk.BonkBot')

class BonkMessage:
    def __init__(self, irc, config, data):
        self.irc = irc
        self.config = config
        self.data = data

    def command(self, cmd):
        return self.data.find('!%s %s' % (self.config['nick'], cmd)) != -1

    def command_args(self, cmd):
        args = self.data.split()
        cmd_args = args[args.index(cmd) + 1:]
        return cmd_args

    def reply(self, message):
        destination = self.channel()
        if destination == self.config['nick']:
            destination = self.author()

        self.say(destination, message)

    def say(self, destination, message):
        self.irc.send('PRIVMSG %s :%s\r\n' % (destination, message))        

    def channel(self):
        return self.data.split()[2]

    def author(self):
        return self.data[1 : self.data.index('!')]

    def admin(self):
        author = self.author()
        for admin in self.config['admins']:
            if admin == author:
                return True
        else:
            return False

class BonkBot:

    def __init__(self, config):
        self.config = config
        self.irc = None

    def connect(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = self.config['host']
        port = int(self.config['port'])
        nick = self.config['nick']
        name = self.config['name']
        channels = self.config['channels']

        LOG.info("Connecting to %s on port %s..." % (host, port))

        self.irc.connect((host, port))

        LOG.info('Connected')
        LOG.info(self.irc.recv(4096))
        LOG.info('Received initial data')

        LOG.info('Sending initial configuration...')
        self.irc.send('NICK %s\r\n' % nick)
        self.irc.send('USER %s 0 * :%s\r\n' % (nick, name))

        for channel in channels:
            self.join(channel)

        LOG.info('Sent initial configuration:')
        LOG.info('  NICK: %s' % nick)
        LOG.info('  USER: %s' % name)
        LOG.info('  JOIN: %s' % channels)

    def listen(self):

        while True:
            data = self.irc.recv(4096)
            if data.find('PING') != -1:
                self.irc.send('PONG ' + data.split()[1] + '\r\n')

            for p in plugins.MSG_PLUGINS:
                message = BonkMessage(self.irc, self.config, data)
                try:
                    p(message)
                except:
                    LOG.exception('Error from plugin [%s]' % p.__name__)

            if message.command('help'):
                message.reply('Greetings traveler. Commands are triggered by typing !, then my name, then the command and any arguments it may have')
                    
                for p in plugins.MSG_PLUGINS:
                    if p.__doc__ is not None:
                        message.reply('   %s' % p.__doc__)

            if message.command('quit'):
                message.irc.send('QUIT :Fine, I\'ll leave...\r\n')

    def start(self):
        self.connect()
        self.listen()

    def startd(self):
        self.connect()
        thread.start_new_thread(self.listen, ())

    def join(self, channel):
        self.irc.send('JOIN %s\r\n' % channel)

