from entts import Room


room_registry = {}

def create_room(roomname):
    if roomname in room_registry:
        return None
    
    room_registry[roomname] = Room(roomname)
    return roomname

def join_room(roomname, username):
    if not roomname in room_registry:
        return None

    room = room_registry[roomname]
    usertoken = room.join(username)
    return usertoken, room.list_users(), None

def leave_room(roomname, usertoken):
    if not roomname in room_registry:
        return None

    room = room_registry[roomname]
    return room.leave(usertoken)

def list_rooms():
    return room_registry.keys()

def send_msg(roomname, usertoken, msg, recipient=None):
    if not roomname in room_registry:
        return False
    
    room = room_registry[roomname]
    return room.send_msg(usertoken, msg, recipient)

def recv_msgs(roomname, usertoken):
    if not roomname in room_registry:
        return None
    
    room = room_registry[roomname]
    return room.recv_msgs(usertoken)

def list_users(roomname):
    if not roomname in room_registry:
        return None
    
    room = room_registry[roomname]
    return room.users()