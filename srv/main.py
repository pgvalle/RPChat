from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os, time, threading
from . import config, functions, entities

exit_evt = threading.Event()

def load_users():
    if os.path.exists('users.dat'):
        pass

# delete rooms after max inactivity time has passed
def refresh_rooms():
    while not exit_evt.is_set():
        for name in entities.rooms.keys():
            room = entities.rooms[name]

            room.time_inactive += 2
            if room.time_inactive >= config.ROOM_MAX_TIME_INACTIVE:
                del entities.rooms[name]

        time.sleep(2)

def main():
    functions.create_room('world')

    #load_users()

    refresh_rooms_th = threading.Thread(target=refresh_rooms, daemon=True)
    refresh_rooms_th.start()

    server = SimpleXMLRPCServer(('localhost', 1444), logRequests=False)
    
    server.register_function(functions.register_user, 'register_user')
    server.register_function(functions.unregister_user, 'unregister_user')
    server.register_function(functions.login, 'login')
    server.register_function(functions.create_room, 'create_room')
    server.register_function(functions.list_users_in_room, 'list_users_in_room')
    server.register_function(functions.list_rooms, 'list_rooms')
    server.register_function(functions.join_room, 'join_room')
    server.register_function(functions.leave_room, 'leave_room')
    server.register_function(functions.send_message, 'send_message')
    server.register_function(functions.receive_messages, 'receive_messages')

    binder = xmlrpc.client.ServerProxy(f'http://localhost:1234')
    binder.register_service('rpchat', 'localhost', 1444)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('bye')

    exit_evt.set()
    refresh_rooms_th.join()
    server.server_close()
