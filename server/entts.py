import utils


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
        self.user_from_token = {}
        self.user_from_name = {}
    
    def join(self, username):
        '''
        Returns token that only the client with username=username will know.
        That prevents a user to maliciously send messages as another one
        '''

        if not username in self.user_from_name:
            return None
        
        user = User(username)

        self.user_from_name[username] = user
        self.user_from_token[user.token] = user
        return user.token

    def leave(self, usertoken):       
        username = self.user_from_name.get(usertoken, None)

        if not username:
            return None

        del self.user_from_token[usertoken]
        del self.user_from_name[username]
        return usertoken

    def send_msg(self, usertoken, msg, recipient=None):
        username = self.user_from_name.get(usertoken, None)

        if not username:
            return False
        
        # TODO send message right here

        return True

    def recv_msgs(self, usertoken):
        return []

    def list_users(self):
        return self.user_from_name.keys()
