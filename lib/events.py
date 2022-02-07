class Event:
    def __init__(self, loop):
        self.listens = {}
        self.loop = loop

    def on(self, name):
        def deco(coro):
            if name in self.listens:
                self.listens[name].append(coro)
            else:
                self.listens[name] = [coro]
        return deco

    def dispatch(self, name, *args, **kwargs):
        if name in self.listens:
            for coro in self.listens[name]:
                self.loop.create_task(coro(*args, **kwargs))