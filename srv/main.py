from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time, threading
from . import functions, entities

def refresh_rooms():
    def is_inactive_5mins(item):
        name, room = item

        if name == 'world' or len(room.users) > 0:
            room.time_inactive = 0
        else:
            room.time_inactive += 2

        return room.time_inactive < 300

    while True:
        before = time.perf_counter()
        entities.rooms = dict(filter(is_inactive_5mins, entities.rooms.items()))

        delta = time.perf_counter() - before
        if delta < 2:
            time.sleep(2 - delta)

def main():
    functions.create_room('world')

    refresh_rooms_th = threading.Thread(target=refresh_rooms, daemon=True)
    refresh_rooms_th.start()

    server = SimpleXMLRPCServer(('127.0.0.1', 1444), logRequests=False, allow_none=True)

    server.register_function(functions.create_user, 'create_user')
    server.register_function(functions.delete_user, 'uncreate_user')
    server.register_function(functions.check_user, 'check_user')
    server.register_function(functions.create_room, 'create_room')
    server.register_function(functions.list_users_in_room, 'list_users_in_room')
    server.register_function(functions.list_rooms, 'list_rooms')
    server.register_function(functions.join_room, 'join_room')
    server.register_function(functions.leave_room, 'leave_room')
    server.register_function(functions.send_message, 'send_message')
    server.register_function(functions.receive_messages, 'receive_messages')

    # binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
    # binder.register_service('rpchat', '127.0.0.1', 1444)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('bye')
    finally:
        server.server_close()
