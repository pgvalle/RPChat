from entts import Room


room_registry = {}

def create_room(roomname):
    '''
    Returns the room token and adm_usertoken if room creation was successful.
    Otherwise, returns None.
    '''

    room = room_registry.get(roomname, None)

    if room:
        return None
    
    room_registry[roomname] = Room(roomname)
    return roomname

def join_room(roomname, username):
    '''
    '''

    room = room_registry.get(roomname, None)

    if not room:
        return None

    usertoken = room.join(username)
    return usertoken, room.list_users(), None

def leave_room(roomname, usertoken):
    '''
    '''

    room = room_registry.get(roomname, None)

    if not room:
        return None

    return room.leave(usertoken)

def list_rooms():
    return room_registry.keys()

def send_msg(roomname, usertoken, msg, recipient=None):
    '''
    Returns True if the message was sent. Otherwise, returns False.
    '''

    room = room_registry.get(roomname, None)

    if not room:
        return False
    
    return room.send_msg(usertoken, msg, recipient)

def recv_msgs(roomname, histsize):
    room = room_registry.get(roomname, None)

    if not room:
        return None
    
    return room.recv_msgs(histsize)

def list_users(roomname):
    room = room_registry.get(roomname, None)

    if not room:
        return None
    
    return room.users()