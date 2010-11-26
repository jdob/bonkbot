import logging

LOG = logging.getLogger('bonk.plugin.log')

def log(message):
    LOG.info(message.data)
