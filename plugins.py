import control
import karma
import log
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
    log.log,
    ops.give,
    personality.insult,
    personality.compliment,
    private_channel.invite,
    stock.stock,
    twitter.twitter,
    weather.weather,
)
