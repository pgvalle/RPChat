from . import statcodes
from . import config
from .entities import *

def is_connection_valid(roomname, username, password):
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND

    if not username in users:
        return statcodes.USER_NOT_FOUND
    
    user = users[username]

    if not user.password == password:
        return statcodes.WRONG_PASSWORD
    
    return statcodes.SUCCESS

# USER STUFF
#########################################################

def register_user(username, password):
    if not User.is_name_valid(username):
        return statcodes.INVALID_USERNAME

    if not User.is_password_valid(password):
        return statcodes.INVALID_PASSWORD

    if username in users:
        return statcodes.USER_EXISTS
    
    if len(users) == config.MAX_USERS:
        return statcodes.USER_REGISTRY_FULL

    users[username] = User(username, password)
    print(f'new user {username} registered')

    return statcodes.SUCCESS

def unregister_user(username, password):
    if not username in users:
        return statcodes.USER_NOT_FOUND
    
    user = users[username]
    
    if user.password != password:
        return statcodes.WRONG_PASSWORD
    
    # for each room the user is, delete them from its userlist
    for _, room in user.rooms:
        del room.users_and_dates[username]

    del users[username] # remove user from global user registry
    print(f'user {username} unregistered')

    return statcodes.SUCCESS

def check(username, password):
    if not username in users:
        return statcodes.USER_NOT_FOUND
    
    user = users[username]

    if user.password != password:
        return statcodes.WRONG_PASSWORD

    return statcodes.SUCCESS

# ROOM STUFF
#########################################################

def create_room(roomname):
    if not Room.is_name_valid(roomname):
        return statcodes.INVALID_ROOMNAME

    if roomname in rooms:
        return statcodes.ROOM_EXISTS
    
    if len(rooms) == config.MAX_ROOMS:
        return statcodes.ROOM_REGISTRY_FULL

    rooms[roomname] = Room()
    print(f'Room {roomname} created')

    return statcodes.SUCCESS

def list_users_in_room(roomname):
    if not roomname in rooms:
        return statcodes.ROOM_NOT_FOUND
    
    room = rooms[roomname]
    return list(room.users_and_dates.keys())

def list_rooms():
    return list(rooms.keys())

# USER AND ROOM STUFF
#########################################################

def join_room(roomname, username, password):
    result = is_connection_valid(roomname, username, password)
    
    if result != statcodes.SUCCESS:
        return result
    
    user = users[username]
    room = rooms[roomname]

    if username in room.users_and_dates:
        print(f'user {username} rejoined {roomname}')
    else:
        invalid_date = datetime.datetime(2000, 1, 1)

        room.users_and_dates[username] = (user, invalid_date)
        user.rooms[roomname] = room
        print(f'user {username} joined {roomname}')

    last_50_messages = []
    i = len(room.messages) - 1

    while i >= 0 and len(room.messages) - i <= 50:
        dest = room.messages[i][3]
        if dest is None:
            last_50_messages.append(room.messages[i])

    users_in_room = list(room.users_and_dates.keys())

    return users_in_room, last_50_messages

def leave_room(roomname, username, password):
    result = is_connection_valid(roomname, username, password)
    
    if result != statcodes.SUCCESS:
        return result
    
    user = users[username]
    room = rooms[roomname]

    if not username in room.users_and_dates:
        return statcodes.USER_NOT_FOUND

    del room.users_and_dates[username] # remove user from room users
    del user.rooms[roomname] # remove room from user rooms
    return statcodes.SUCCESS

def send_message(roomname, username, password, message, recipient=None):
    result = is_connection_valid(roomname, username, password)
    
    if result != statcodes.SUCCESS:
        return result
    
    room = rooms[roomname]

    if not username in room.users_and_dates:
        return statcodes.USER_NOT_FOUND
    
    if not recipient in room.users_and_dates:
        return statcodes.RECIPIENT_NOT_FOUND
    
    room.send_message(username, message, recipient)
    return statcodes.SUCCESS

def receive_messages(roomname, username, password):
    result = is_connection_valid(roomname, username, password)
    
    if result != statcodes.SUCCESS:
        return result

    room = rooms[roomname]

    if not username in room.users_and_dates:
        return statcodes.USER_NOT_FOUND
    
    _, adate = room.users_and_dates[username]
    last_messages = []
    i = len(room.messages) - 1

    while i >= 0:
        date = room.messages[i][0]

        if adate >= date: # may cause trouble bc of >=
            break

        last_messages.append(room.messages[i])

    return last_messages
