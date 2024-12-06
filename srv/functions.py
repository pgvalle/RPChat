from . import statcodes
from . import config
from .entities import *

def is_connection_valid(roomname, username, auth_token):
    if not roomname in rooms_by_name:
        return statcodes.ROOM_NOT_FOUND

    if not username in users_by_name:
        return statcodes.USER_NOT_FOUND

    user = users_by_name[username]

    if user.auth_token != auth_token:
        return statcodes.USER_SESSION_ERROR
    
    return statcodes.SUCCESS

# USER STUFF
#########################################################

def register_user(username, password):
    if not User.is_name_valid(username):
        return statcodes.INVALID_USERNAME

    if not User.is_password_valid(password):
        return statcodes.INVALID_PASSWORD

    if username in users_by_name:
        return statcodes.USER_EXISTS
    
    if len(users_by_name) == config.MAX_USERS:
        return statcodes.USER_REGISTRY_FULL

    users_lock.acquire()
    users_by_name[username] = User(username, password)
    print(f'New user {username} registered')
    users_lock.release()

    return statcodes.SUCCESS

def unregister_user(username, password):
    if not User.is_name_valid(username) or not username in users_by_name:
        return statcodes.USER_NOT_FOUND
    
    user = users_by_name[username]
    
    if user.password != password:
        return statcodes.WRONG_PASSWORD
    
    # for each room the user is, delete them from its userlist
    for _, room in user.rooms_by_name:
        del room.users_by_name[username]

    users_lock.acquire()
    del users_by_name[username] # remove user from global user registry
    print(f'User {username} unregistered')
    users_lock.release()

    return statcodes.SUCCESS

def login(username, password):
    if not username in users_by_name:
        return statcodes.USER_NOT_FOUND
    
    user = users_by_name[username]

    if user.password != password:
        return statcodes.WRONG_PASSWORD

    # everytime the client calls login, generate a new auth_token
    # It invalidates any other token created previously
    print(f'User {username} created a new session')
    return user.refresh_auth_token()

# ROOM STUFF
#########################################################

def create_room(roomname):
    if not Room.is_name_valid(roomname):
        return statcodes.INVALID_ROOMNAME

    if roomname in rooms_by_name:
        return statcodes.ROOM_EXISTS
    
    if len(rooms_by_name) == config.MAX_ROOMS:
        return statcodes.ROOM_REGISTRY_FULL

    rooms_lock.acquire()
    rooms_by_name[roomname] = Room()
    print(f'Room {roomname} created')
    rooms_lock.release()

    return statcodes.SUCCESS

def list_users_in_room(roomname):
    if not roomname in rooms_by_name:
        return statcodes.ROOM_NOT_FOUND
    
    room = rooms_by_name[roomname]
    return list(room.users_by_name.keys())

def list_rooms():
    return list(rooms_by_name.keys())

# USER AND ROOM STUFF
#########################################################

def join_room(roomname, username, auth_token):
    result = is_connection_valid(roomname, username, auth_token)
    
    if result != statcodes.SUCCESS:
        return result
    
    user = users_by_name[username]
    room = rooms_by_name[roomname]

    if username in room.users_by_name:
        return statcodes.USER_EXISTS

    room.users_by_name[username] = user # add user to room users
    user.rooms_by_name[roomname] = room # add room to user rooms
    print(f'{username} joined {roomname}')

    users_in_room = list(room.users_by_name.keys())
    last_50_messages = []

    i = len(room.messages) - 1
    while i >= 0 and len(room.messages) - i <= 50:
        dest = room.messages[i][3]
        if dest is None:
            last_50_messages.append(room.messages[i])

    return users_in_room, last_50_messages

def leave_room(roomname, username, auth_token):
    result = is_connection_valid(roomname, username, auth_token)
    
    if result != statcodes.SUCCESS:
        return result
    
    user = users_by_name[username]
    room = rooms_by_name[roomname]

    if not username in room.users_by_name:
        return statcodes.USER_NOT_FOUND

    del room.users_by_name[username] # remove user from room users
    del user.rooms_by_name[roomname] # remove room from user rooms
    return statcodes.SUCCESS

def send_message(roomname, username, auth_token, message, recipient=None):
    result = is_connection_valid(roomname, username, auth_token)
    
    if result != statcodes.SUCCESS:
        return result
    
    room = rooms_by_name[roomname]

    if not username in room.users_by_name:
        return statcodes.USER_NOT_FOUND
    
    if not recipient in room.users_by_name:
        return statcodes.RECIPIENT_NOT_FOUND
    
    room.send_message(username, message, recipient)
    return statcodes.SUCCESS

def receive_messages(roomname, username, auth_token):
    result = is_connection_valid(roomname, username, auth_token)
    
    if result != statcodes.SUCCESS:
        return result
    
    user = users_by_name[username]
    room = rooms_by_name[roomname]

    if not username in room.users_by_name:
        return statcodes.USER_NOT_FOUND
    
    return -1234512893
    

'''
`join_room(username, room_name)`
  ```
  Permite que o usuário entre em uma sala existente. Anuncia a entrada do usuário para todos.
  Retorna A lista de usuários conectados na sala e as últimas 50 mensagens públicas (broadcast) da sala.
  ```
* `send_message(username, room_name, message, recipient=None)`
  ```
  Envia uma mensagem pública se recipient=None. Caso contrário, a mensagem é enviada apenas para o destinatário especificado.
  ```
* `receive_messages(username, room_name)`
'''