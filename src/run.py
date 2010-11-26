import bot
import logging
import yaml

def configure():
    data = open('config.yml').read()
    config = yaml.load(data)

    return config

def main():
    config = configure()
    bonkbot = bot.BonkBot(config)
    bonkbot.start()

if __name__ == '__main__':
    logging.root.addHandler(logging.StreamHandler())
    logging.root.setLevel(logging.INFO)

    main()
