from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import rpchat
import config

if __name__ == '__main__':
    # Configura o servidor
    server = SimpleXMLRPCServer((config.HOST, config.PORT - 1))

    server.register_function(rpchat.create_room, 'create_room')
    server.register_function(rpchat.join_room, 'join_room')
    server.register_function(rpchat.leave_room, 'leave_room')
    server.register_function(rpchat.list_rooms, 'list_rooms')
    server.register_function(rpchat.send_msg, 'send_msg')
    server.register_function(rpchat.recv_msgs, 'recv_msgs')
    server.register_function(rpchat.list_users, 'list_users')

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy(f'http://{config.HOST}:{config.PORT}')
    binder.register_procedure('rpchat', config.PORT - 1)

    print('RPChat ready to rock')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('bye')