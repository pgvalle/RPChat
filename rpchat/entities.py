from . import utils, statcodes


class User:
    '''An inactive user is one that is neither calling get_mgs nor send_msg.'''

    MAX_INACTIVE_TIME = 10
    
    def __init__(self, name):
        self.name = name
        self.token = utils.create_token(size=32)
        self.time_inactive = 0
    
    def should_be_kicked(self):
        return self.time_inactive >= User.MAX_INACTIVE_TIME


class Room:

    HIST_MAX_SIZE = 50

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
        '''Returns token that only the client with username=username will know.
        That token is to ensure that the user is themself.'''

        if username in self.user_from_name:
            self.log(f'{username} already taken')
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
        
        user = self.user_from_token(usertoken)

        del self.user_from_name[user.name]
        del self.user_from_token[user.token]
        self.log(f'{user.name} left')

        return statcodes.SUCCESS

    def send_msg(self, usertoken, msg, recipient=None):
        if not usertoken in self.user_from_token:
            self.log(f'someone that is not in the room tried to send a message')
            return statcodes.USER_NOT_FOUND
        
        user = self.user_from_token(usertoken)
        self.log(f'{user.name} sent a message')
        # TODO send message right here

        return statcodes.SUCCESS

    def recv_msgs(self, usertoken):
        if not usertoken in self.user_from_token:
            return statcodes.USER_NOT_FOUND
        
        user = self.user_from_token(usertoken)

        # TODO implement recv messages

        return []

    def list_users(self):
        return list(self.user_from_name.keys())
