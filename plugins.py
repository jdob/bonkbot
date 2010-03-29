import control
import karma
import log
import ops
import personality
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
    stock.stock,
    twitter.twitter,
    weather.weather,
)
