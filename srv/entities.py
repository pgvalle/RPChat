import uuid, datetime, threading

class User:

    def __init__(self, name, password):
        self.rooms = {}
        self.name = name
        self.password = password
        self.auth_token = 0

    def refresh_auth_token(self):
        self.auth_token = str(uuid.uuid4())
        return self.auth_token
    
    def __str__(self):
        '''To serialize user to file'''
        return f'{self.name} {self.password}'
    
    @staticmethod
    def is_name_valid(name):
        return True
    
    @staticmethod
    def is_password_valid(password):
        return True
    
# store registered users and their tokens
users = {}

class Room:

    def __init__(self):
        self.users_and_dates = {}
        self.messages = []
        self.time_inactive = 0

    def send_message(self, orig, content, dest=None):
        now = datetime.datetime.now()
        self.messages.append((now, orig, content, dest))

    @staticmethod
    def is_name_valid(name):
        return True
    
# store rooms
rooms = {}