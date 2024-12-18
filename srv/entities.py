import datetime

class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.rooms = {}  # self.rooms['room'] = time_last_call_2_receive_messages
    
# store registered users
users = {}

class Room:

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.inactivity = 0
        self.users = {}

    def send_message(self, orig, content, dest):
        now = datetime.datetime.now()
        self.messages.insert(0, (now, orig, content, dest))

    def update_inactivity(self, seconds):
        if self.name == 'world' or len(self.room.users) > 0:
            self.inactivity = 0
        else:
            self.inactivity += seconds

        return self.inactivity < 300
    
# store rooms
rooms = {}