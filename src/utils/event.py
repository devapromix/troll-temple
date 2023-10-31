class Event:
    def __init__(self):
        self.subscribers = []

    def __iadd__(self, f):
        self.subscribers.append(f)
        return self

    def __isub__(self, f):
        self.subscribers.remove(f)
        return self

    def invoke(self, *args):
        for subscriber in self.subscribers:
            subscriber(*args)
