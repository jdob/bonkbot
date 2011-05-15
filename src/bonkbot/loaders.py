#!/usr/bin/python
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from ConfigParser import SafeConfigParser
import imp
import logging
import os


LOG = logging.getLogger(__name__)


class InstalledPluginLoader:

    def __init__(self, bot_config_filename, conf_dir='/etc/bonkbot/conf.d', plugin_dir='/etc/bonkbot/plugins'):
        self.bot_config_filename = bot_config_filename
        self.conf_dir = conf_dir
        self.plugin_dir = plugin_dir


    def load(self, irc_client):

        # Find each plugin to load by the entries in the conf dir
        conf_files = [f for f in os.listdir(self.conf_dir) if f.endswith('.conf')]

        all_listeners = []

        for conf_file in conf_files:
            plugin_name = conf_file.split('.')[0]
            full_path = os.path.join(self.conf_dir, conf_file)

            plugin_conf = SafeConfigParser()
            plugin_conf.read([self.bot_config_filename, full_path])

            if not plugin_conf.has_section('plugin') or not plugin_conf.has_option('plugin', 'enabled'):
                LOG.warning('Could not find enabled property for plugin configuration [%s]' % full_path)
                continue

            if not plugin_conf.getboolean('plugin', 'enabled'):
                LOG.info('Skipping disabled plugin [%s]' % plugin_name)

            try:
                plugin_module = self._load_module(plugin_name)
                listeners = plugin_module.init_plugin(plugin_conf, irc_client)
                all_listeners += listeners
            except Exception:
                LOG.exception('Error initializing plugin [%s]' % plugin_name)
                continue

        return all_listeners

    def _load_module(self, plugin_name):
        source_file = os.path.join(self.plugin_dir, plugin_name + '.py')
        module = imp.load_source(plugin_name, source_file)
        return module