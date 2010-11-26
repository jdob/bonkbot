#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

class command:
    '''
    Runs the function if the given command was indicated to the bot.
    '''

    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            message = args[0]
            if message.command(self.name):
                f(*args)
        wrapped.__doc__ = f.__doc__
        return wrapped

class admin:
    '''
    Runs the function only if the author giving the command is registered as an admin.
    '''

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        message = args[0]
        if message.admin():
            self.f(*args)
