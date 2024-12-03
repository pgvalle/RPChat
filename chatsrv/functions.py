from . import room, statcodes


user_registry = []
room_registry = {}


def create_room(roomname):
    # room must not exist yet
    if roomname in room_registry:
        return statcodes.ROOM_EXISTS
    
    room_registry[roomname] = room.Room(roomname)

    return statcodes.SUCCESS


def join_room(roomname, username):
    # If user doesn't exist, create it
    if not username in user_registry:
        user_registry.append(username)

    # room must exist
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND

    # get room and add user to it
    room = room_registry[roomname]
    return room.join(username)


def list_rooms():
    return list(room_registry.keys())


def send_msg(roomname, username, msg, recipient=None):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    return room.send_msg(username, msg, recipient)


def recv_msgs(roomname, username):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    return room.recv_msgs(username)


def list_users(roomname):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    return room.users