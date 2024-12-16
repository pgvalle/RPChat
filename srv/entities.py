import datetime

class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.rooms = {}
    
# store registered users
users = {}

class Room:

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.time_inactive = 0
        self.users = {}

    def send_message(self, orig, content, dest):
        now = datetime.datetime.now()
        self.messages.insert(0, (now, orig, content, dest))
    
# store rooms
rooms = {}