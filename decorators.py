class command:

    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            message = args[0]
            if message.command(self.name):
                f(*args)
        return wrapped

class admin:

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        message = args[0]
        if message.admin():
            self.f(*args)
