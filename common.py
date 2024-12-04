from datetime import datetime

class Message:

    def __init__(self, orig, dest, content):
        self.orig = orig
        self.dest = dest
        self.content = content
        self.date = datetime.now()

    def is_public(self):
        return self.dest is None

    def __str__(self):
        return self.content
