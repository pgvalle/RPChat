TOKEN_CHARS = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?@#$%&*')

def create_token(size):
    from random import choices
    
    token_as_list = choices(TOKEN_CHARS, k=size)
    return ''.join(token_as_list)


class Room:
    '''
    Room.users is a dictionary of pairs {usertoken: username}
    '''

    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.user2token = {}
        self.token2user = {}
        self.hist = []


name2room = {}
token2room = {}


def create_room(name):
    '''Returns the room token if room creation was successful.
    Otherwise, returns an empty string.'''

    if name in name2room:
        return ''
    
    token = create_token(size=16)

    room = Room(name, token)
    token2room[token] = room
    name2room[name] = room
    return token


def destroy_room(token):
    '''
    Returns the room token if room existed and was destroyed.
    Otherwise, returns an empty string.
    '''

    if not token in token2room:
        return ''

    name = token2room[token].name

    del name2room[name], token2room[token]
    return token


def join_room(name, username):
    '''
    Returns the token of the new user, the list of users in the room
    and last 50 public messages on success. Otherwise, returns None.
    '''

    if not name in name2room:
        return None
    
    room = name2room[name]

    if username in room.user2token:
        return None
    
    usertoken = create_token(size=32)
    room.user2token[username] = usertoken
    room.token2user[usertoken] = username

    usernames = room.user2token.keys()
    return usertoken, usernames, None


def leave_room(name, usertoken):
    pass


def list_rooms():
    return name2room.keys()


def list_users(roomname):
    '''
    Returns the room's user list if the room exists. Otherwise, returns None.
    '''

    if not roomname in name2room:
        return None
    
    return name2room[roomname].user2token.keys()


def send_msg(usertoken, roomname, msg, recipient=None):
    '''
    Returns True if the message was sent. Otherwise, returns False.
    '''

    if not roomname in name2room:
        return False
    
    room = name2room[roomname]

    if not usertoken in room.token2user:
        return False
    
    recipient = 'all' if recipient == None else recipient
    print(f'{msg} sent to {recipient}')