from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import rpchat
import sys


def main():
    if len(sys.argv) < 4:
        print('Expected binder host, binder port and server host')
        return
    
    binder_host, binder_port = None, None
    server_host = None

    try:
        binder_host, binder_port = sys.argv[1], int(sys.argv[2])
        server_host = sys.argv[3]
    except Exception as e:
        print(f'Error when parsing arguments: {e}')
        return

    # configure server
    try:
        server = SimpleXMLRPCServer((server_host, 0))
        server_port = server.server_address[1]
    except Exception as e:
        print(f'Error when creating server: {e}')
        return
    
    server.register_function(rpchat.create_room, 'create_room')
    server.register_function(rpchat.join_room, 'join_room')
    server.register_function(rpchat.leave_room, 'leave_room')
    server.register_function(rpchat.list_rooms, 'list_rooms')
    server.register_function(rpchat.send_msg, 'send_msg')
    server.register_function(rpchat.recv_msgs, 'recv_msgs')
    server.register_function(rpchat.list_users, 'list_users')

    # configure connection to binder
    try:
        binder = xmlrpc.client.ServerProxy(f'http://{binder_host}:{binder_port}')
        binder.register_procedure('rpchat', server_host, server_port)
    except Exception as e:
        print(f'Error when connecting to binder: {e}')
        print(f'Service will still be available at {server_host}:{server_port}')

    print(f'RPChat ready')

    # keep server running
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('bye')


if __name__ == '__main__':
    main()