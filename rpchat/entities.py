from . import utils, statcodes, config


class User:
    
    def __init__(self, name):
        self.name = name
        self.token = utils.create_token(size=32)
        self.time_inactive = 0
    
    def should_be_kicked(self):
        return self.time_inactive >= config.USER_MAX_TIME_INACTIVE


class Room:

    def __init__(self, name):
        self.name = name
        self.history = []
        self.time_inactive = 0

        # redundancy so that all operations are quick
        self.user_from_name = {}
        self.user_from_token = {}

    def log(self, msg):
        print(f'{self.name}: {msg}')
    
    def join(self, username):
        if len(self.user_from_name) == config.ROOM_MAX_USERS:
            return statcodes.ROOM_FULL

        if username in self.user_from_name:
            self.log(f'someone tried to join as {username}')
            return statcodes.USER_EXISTS

        user = User(username)

        self.user_from_name[user.name] = user
        self.user_from_token[user.token] = user
        self.log(f'{username} joined')

        return user.token

    def leave(self, usertoken):
        if not usertoken in self.user_from_token:
            self.log(f'someone that is not in the room tried to leave')
            return statcodes.USER_NOT_FOUND
        
        user = self.user_from_token[usertoken]

        del self.user_from_name[user.name]
        del self.user_from_token[user.token]
        self.log(f'{user.name} left')

        return statcodes.SUCCESS

    def send_msg(self, usertoken, msg, recipient=None):
        if not usertoken in self.user_from_token:
            self.log(f'someone that is not in the room tried to send a message')
            return statcodes.USER_NOT_FOUND
        
        user = self.user_from_token[usertoken]
    
        self.log(f'{user.name} sent \'{msg}\'')
        # TODO send message right here

        return statcodes.SUCCESS

    def recv_msgs(self, usertoken):
        if not usertoken in self.user_from_token:
            return statcodes.USER_NOT_FOUND
        
        user = self.user_from_token[usertoken]

        # TODO implement recv messages

        return []

    def list_users(self):
        return list(self.user_from_name.keys())
