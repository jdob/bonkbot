#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

from ConfigParser import SafeConfigParser
from loaders import InstalledPluginLoader
import logging
from optparse import OptionParser
import os

import bot


DEFAULT_CONF_FILE = '/etc/bonkbot/bonk.conf'

USER_LOG_DIR = '~/.bonkbot'
USER_LOG_FILE = 'bonkbot.log'


def load_configuration(filename):
    config = SafeConfigParser()
    config.read(filename)
    return config


def configure_logging(log_dir=None, debug=False):

    # Determine log file location
    if not log_dir:
        log_dir = os.path.expanduser(USER_LOG_DIR)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, USER_LOG_FILE)

    # Configure the root level logger so plugins get it too
    logger = logging.root

    handler = logging.FileHandler(log_file, mode='w')
    logger.addHandler(handler)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def launch():

    # Command line options
    parser = OptionParser()
    parser.add_option('-v', dest='debug', action='store_true', default='True',
                      help='write verbose information to the logs')
    parser.add_option('-c', '--config', dest='config_file', default=DEFAULT_CONF_FILE,
                      help='full path to the bot config file')

    options, args = parser.parse_args()

    # Configuration
    config = load_configuration(options.config_file)

    # Logging
    log_dir = None
    if config.has_option('bot', 'log_dir'): log_dir = config.get('bot', 'log_dir')
    configure_logging(log_dir=log_dir, debug=options.debug)

    # Bot Creation
    loader = InstalledPluginLoader(options.config_file, config.get('plugins', 'conf_dir'), config.get('plugins', 'module_dir'))
    bonkbot = bot.BonkBot(config, loader)

    # Run
    bonkbot.start()


if __name__ == '__main__':
    launch()
