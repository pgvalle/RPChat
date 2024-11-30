from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import services
from .. import config


if __name__ == '__main__':
    # Configura o servidor
    server = SimpleXMLRPCServer((config.HOST, config.HIDDEN_PORT))
    print('RPChat ready')

    # Registra as funções
    server.register_function(services.create_room, 'create_room')
    server.register_function(services.join_room, 'join_room')
    server.register_function(services.leave_room, 'leave_room')
    server.register_function(services.list_rooms, 'list_rooms')
    server.register_function(services.send_msg, 'send_msg')
    server.register_function(services.recv_msgs, 'recv_msgs')
    server.register_function(services.list_users, 'list_users')

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy(f'http://{config.HOST}:{config.PORT}')
    binder.register_service('rpchat', config.HIDDEN_PORT)

    # Mantém o servidor em execução
    server.serve_forever()