#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from decorators import command

@command('invite')
def invite(message):
    '''invite [channel_name] [user] [user] ...'''

    args = message.command_args('invite')

    channel = args[0]
    invitees = args[1:]
    topic = '%s channel created by %s' % (message.config['name'], message.author())

    message.irc.send('JOIN %s\r\n' % channel)
    message.irc.send('TOPIC %s :%s\r\n' % (channel, topic))

    for person in invitees:
        message.irc.send('INVITE %s %s\r\n' % (person, channel))
