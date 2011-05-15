#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from bonkbot.decorators import command, admin


def init_plugin(config, irc_client):
    return [speak, join, leave]

@command('speak')
@admin
def speak(message):
    cmd_args = message.command_args('speak')
    channel = cmd_args[0]
    speak_args = cmd_args[1:]
    say_this = ' '.join(speak_args)

    message.irc_client.senf(channel, say_this)

@command('join')
@admin
def join(message):
    cmd_args = message.command_args('join')
    channel = cmd_args[0]
    message.irc_client.join(channel)

@command('leave')
@admin
def leave(message):
    cmd_args = message.command_args('leave')
    channel = cmd_args[0]
    message.irc_client.leave(channel)
