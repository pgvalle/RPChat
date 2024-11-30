from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from . import functions
from .. import config


if __name__ == '__main__':
    # Configura o servidor
    server = SimpleXMLRPCServer((config.HOST, config.PORT - 1))
    print('RPChat ready')

    # Registra as funções
    server.register_function(functions.create_room, 'create_room')
    server.register_function(functions.join_room, 'join_room')
    server.register_function(functions.leave_room, 'leave_room')
    server.register_function(functions.list_rooms, 'list_rooms')
    server.register_function(functions.send_msg, 'send_msg')
    server.register_function(functions.recv_msgs, 'recv_msgs')
    server.register_function(functions.list_users, 'list_users')

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy(f'http://{config.HOST}:{config.PORT}')
    binder.register_service('rpchat', config.PORT - 1)

    # Mantém o servidor em execução
    server.serve_forever()