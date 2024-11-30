from . import entities, statcodes


MAX_ROOMS = 1000

room_registry = {}


def create_room(roomname):
    if roomname in room_registry:
        return statcodes.ROOM_EXISTS
    
    if len(room_registry) == MAX_ROOMS:
        return statcodes.ROOM_REGISTRY_FULL

    room_registry[roomname] = entities.Room(roomname)
    return statcodes.SUCCESS


def join_room(roomname, username):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND

    room = room_registry[roomname]
    return room.join(username), room.list_users()


def leave_room(roomname, usertoken):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND

    room = room_registry[roomname]
    return room.leave(usertoken)


def list_rooms():
    return list(room_registry.keys())


def send_msg(roomname, usertoken, msg, recipient=None):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    return room.send_msg(usertoken, msg, recipient)


def recv_msgs(roomname, usertoken):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    return room.recv_msgs(usertoken)


def list_users(roomname):
    if not roomname in room_registry:
        return statcodes.ROOM_NOT_FOUND
    
    room = room_registry[roomname]
    userlist = room.list_users()
    return ' '.join(userlist)