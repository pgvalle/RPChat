from . import statcodes
from .entities import *

def _check_user(username, password):
    if not username in users:
        return None
    
    user = users[username]
    return user if user.password == password else None

# USER STUFF
#########################################################

def create_user(username, password):    
    if username in users:
        return statcodes.INVALID_CREDENTIALS
    
    users[username] = User(username, password)
    print(f'new user {username} registered')

    return statcodes.SUCCESS

def delete_user(username, password):
    user = _check_user(username, password)

    if not user:
        return statcodes.INVALID_CREDENTIALS
    
    # for each room the user is, delete them from its userlist
    for room, _ in user.rooms.values():
        del room.users[username]

    del users[username]
    print(f'user {username} unregistered')

    return statcodes.SUCCESS

def check_user(username, password):
    user = _check_user(username, password)
    return statcodes.SUCCESS if user else statcodes.INVALID_CREDENTIALS

# ROOM STUFF
#########################################################

def create_room(roomname):
    if roomname in rooms:
        return statcodes.INVALID_ROOM

    rooms[roomname] = Room(roomname)
    print(f'room {roomname} created')

    return statcodes.SUCCESS

def list_users_in_room(roomname):
    if not roomname in rooms:
        return statcodes.INVALID_ROOM
    
    room = rooms[roomname]
    return list(room.users.keys())

def list_rooms():
    return list(rooms.keys())

# USER AND ROOM STUFF
#########################################################

def join_room(roomname, username, password):
    if not roomname in rooms:
        return statcodes.INVALID_ROOM

    room = rooms[roomname]
    user = _check_user(username, password)
    
    if not user:
        return statcodes.INVALID_CREDENTIALS

    if username in room.users:
        now = datetime.datetime.now()

        user.rooms[roomname] = room, now
        print(f'user {username} rejoined {roomname}')
    else:
        epoch = datetime.datetime.fromtimestamp(0)

        room.users[username] = user
        user.rooms[roomname] = room, epoch
        print(f'user {username} joined {roomname}')

    users_in_room = list(room.users.keys())
    last50messages = []

    for message in room.messages:
        if not message[3]:  # only public messages
            last50messages.insert(0, message)

        if len(last50messages) == 50:
            break

    return users_in_room, last50messages

def leave_room(roomname, username, password):
    if not roomname in rooms:
        return statcodes.INVALID_ROOM

    room = rooms[roomname]
    user = _check_user(username, password)
    
    if not user:
        return statcodes.INVALID_CREDENTIALS
    
    if not username in room.users:
        return statcodes.USER_NOT_FOUND

    del room.users[username]
    del user.rooms[roomname]
    return statcodes.SUCCESS

def send_message(roomname, username, password, content, dest=None):
    if not roomname in rooms:
        return statcodes.INVALID_ROOM

    room = rooms[roomname]
    user = _check_user(username, password)
    
    if not user:
        return statcodes.INVALID_CREDENTIALS

    if not username in room.users:
        return statcodes.USER_NOT_FOUND
    
    if dest and not dest in room.users:
        return statcodes.RECIPIENT_NOT_FOUND

    room.send_message(username, content, dest)
    return statcodes.SUCCESS

def receive_messages(roomname, username, password):
    if not roomname in rooms:
        return statcodes.INVALID_ROOM

    room = rooms[roomname]
    user = _check_user(username, password)
    
    if not user:
        return statcodes.INVALID_CREDENTIALS

    if not username in room.users:
        return statcodes.USER_NOT_FOUND

    _, date_last_update = user.rooms[roomname]
    last_messages = []

    for message in room.messages:
        date, _, _, dest = message

        if date <= date_last_update:  # only messages between last update and now
            break
        
        if not dest or dest == username:  # only messages to this user or public ones
            last_messages.insert(0, message)

    return last_messages
