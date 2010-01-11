from config import *

def log(irc, data):
    if len(data) > 0:
        print(data.rstrip())
