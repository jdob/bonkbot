#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import control
import karma
import ops
import personality
import private_channel
import stock
import twitter
import weather

MSG_PLUGINS = (
    control.speak,
    control.join,
    control.leave,
    karma.karma,
    ops.give,
    personality.insult,
    personality.compliment,
    private_channel.invite,
    stock.stock,
    twitter.twitter,
    weather.weather,
)

INIT_PLUGINS = (
    karma.load,
)