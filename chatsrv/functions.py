from . import room, statcodes


users = []
rooms = {}


def create_room(roomname):
    # room must not exist yet
    if roomname in rooms:
        return statcodes.ROOM_EXISTS
    
    rooms[roomname] = room.Room(roomname)

    return statcodes.SUCCESS


def join_room(roomname, username):
    # If user doesn't exist, create it
    if not username in users:
        users.append(username)

    # room must exist
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND

    # get room and add user to it
    room = rooms[roomname]
    return room.join(username)


def list_rooms():
    return list(rooms.keys())


def send_msg(roomname, username, msg, recipient=None):
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND
    
    room = rooms[roomname]
    return room.send_msg(username, msg, recipient)


def recv_msgs(roomname, username):
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND
    
    room = rooms[roomname]
    return room.recv_msgs(username)


def list_users(roomname):
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND
    
    room = rooms[roomname]
    return room.users
