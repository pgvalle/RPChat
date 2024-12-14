import uuid, datetime, threading

class User:

    def __init__(self, name, password):
        self.rooms = {}
        self.name = name
        self.password = password
    
    def __str__(self):
        '''To serialize user to file'''
        return f'{self.name} {self.password}'
    
    @staticmethod
    def is_name_valid(name):
        return len(name) >= 2 and len(name) <= 16
    
    @staticmethod
    def is_password_valid(password):
        return len(password) >= 4 and len(password) <= 16
    
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
        return len(name) >= 2 and len(name) <= 16
    
# store rooms
rooms = {}