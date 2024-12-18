from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import sys, time, threading
from . import functions, entities

def refresh_rooms():
    delta = 0
    room_filter = lambda item: item[1].update_inactivity(delta)

    while True:
        before = time.perf_counter()
        entities.rooms = dict(filter(room_filter, entities.rooms.items()))
        delta = time.perf_counter() - before
        
        if delta < 2:
            time.sleep(2 - delta)
            delta += 2 - delta

def parse_cli_args():
    if len(sys.argv) < 5:
        print('Expected host and port for server, then binder')
        exit(1)
    
    try:
        addr = sys.argv[1], int(sys.argv[2])
        binder_addr = sys.argv[3], int(sys.argv[4])
        return addr, binder_addr
    except Exception as e:
        print(f'Error parsing arguments: {e}')
        exit(2)

def main():
    addr, binder_addr = parse_cli_args()

    functions.create_room('world')

    refresh_rooms_th = threading.Thread(target=refresh_rooms, daemon=True)
    refresh_rooms_th.start()

    try:
        server = SimpleXMLRPCServer(addr, logRequests=False, allow_none=True)
    except Exception as e:
        print(f'Error creating server: {e}')
        exit(3)

    server.register_function(functions.create_user, 'create_user')
    server.register_function(functions.delete_user, 'delete_user')
    server.register_function(functions.check_user, 'check_user')
    server.register_function(functions.create_room, 'create_room')
    server.register_function(functions.list_users_in_room, 'list_users_in_room')
    server.register_function(functions.list_rooms, 'list_rooms')
    server.register_function(functions.join_room, 'join_room')
    server.register_function(functions.leave_room, 'leave_room')
    server.register_function(functions.send_message, 'send_message')
    server.register_function(functions.receive_messages, 'receive_messages')

    try:
        binder = xmlrpc.client.ServerProxy(f'http://{binder_addr[0]}:{binder_addr[1]}')
        binder.register_service('rpchat', addr[0], server.server_address[1])
    except Exception as e:
        print(f'Error connecting to binder: {e}')
        exit(4)

    print('Server ready')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('bye')
    finally:
        server.server_close()
