#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import socket

class IRCClient():
    '''
    Sends the appropriate IRC calls for various IRC related operations.
    '''

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port, nick, name):
        self.socket.connect((host, port))
        self.socket.recv(4096)
        self.nick(nick)
        self.user(nick, name)
        
    def send(self, destination, message):
        self.socket.send('PRIVMSG %s :%s\r\n' % (destination, message))

    def receive(self):
        return self.socket.recv(4096)

    def join(self, channel):
        self.socket.send('JOIN %s\r\n' % channel)

    def leave(self, channel):
        self.socket.send('PART %s\r\n' % channel)

    def give_ops(self, channel, user):
        self.socket.send('MODE ' + channel + ' +o ' + user + '\r\n')

    def nick(self, nick):
        self.socket.send('NICK %s\r\n' % nick)

    def user(self, nick, name):
        self.socket.send('USER %s 0 * :%s\r\n' % (nick, name))

    def quit(self, message):
        self.socket.send('QUIT :%s\r\n' % message)

    def topic(self, channel, topic):
        self.socket.send('TOPIC %s :%s\r\n' % (channel, topic))

    def invite(self, channel, user):
        self.socket.send('INVITE %s %s\r\n' % (user, channel))

    def raw(self, command):
        self.socket.send(command)