from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from service import functions
import config

if __name__ == '__main__':
    # Configura o servidor
    rpchat_server = SimpleXMLRPCServer((config.HOST, config.PORT - 1))
    print('RPChat ready')

    # Registra as funções
    rpchat_server.register_function(functions.create_room, 'create_room')
    rpchat_server.register_function(functions.join_room, 'join_room')
    rpchat_server.register_function(functions.leave_room, 'leave_room')
    rpchat_server.register_function(functions.list_rooms, 'list_rooms')
    rpchat_server.register_function(functions.send_msg, 'send_msg')
    rpchat_server.register_function(functions.recv_msgs, 'recv_msgs')
    rpchat_server.register_function(functions.list_users, 'list_users')

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy(f'http://{config.HOST}:{config.PORT}')
    binder.register_procedure('rpchat', config.PORT - 1)

    try:
        # Mantém o servidor em execução
        rpchat_server.serve_forever()
    except KeyboardInterrupt:
        print('bye')