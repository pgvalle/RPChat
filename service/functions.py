from . import entities


room_registry = {}

NOT_IN_REGISTRY = 1
INVALID = 2


def __validate_room(roomname):
    if not isinstance(roomname, str):
        return INVALID
    
    if not roomname in room_registry:
        return NOT_IN_REGISTRY
    
    return 0

def create_room(roomname):
    code = __validate_room(roomname)

    if code == NOT_IN_REGISTRY:
        room_registry[roomname] = entities.Room(roomname)
        return 0
    
    if code == INVALID:
        return INVALID

    return code

def join_room(roomname, username):
    code = __validate_room(roomname)
    
    if code != 0:
        return code

    room = room_registry[roomname]
    usertoken = room.join(username)
    return usertoken, room.list_users(), None

def leave_room(roomname, usertoken):
    code = __validate_room(roomname)
    
    if code != 0:
        return code

    room = room_registry[roomname]
    return room.leave(usertoken)

def list_rooms():
    return list(room_registry.keys())

def send_msg(roomname, usertoken, msg, recipient=None):
    code = __validate_room(roomname)
    
    if code != 0:
        return code
    
    room = room_registry[roomname]
    return room.send_msg(usertoken, msg, recipient)

def recv_msgs(roomname, usertoken):
    code = __validate_room(roomname)
    
    if code != 0:
        return code
    
    room = room_registry[roomname]
    return room.recv_msgs(usertoken)

def list_users(roomname):
    code = __validate_room(roomname)
    
    if code != 0:
        return code
    
    room = room_registry[roomname]
    return room.list_users()