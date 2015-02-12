#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from bonkbot.bot.decorators import join


def init_plugin(config, irc_client):
    return [give]


@join
def give(message):
    new_op = message.author()

    # Don't try to op yourself
    if new_op != message.config.get('bot', 'nick'):
        message.irc_client.give_ops(message.channel()[1:], message.author())
