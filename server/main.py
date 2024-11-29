from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import services


HOST, PORT = 'localhost', 12345

if __name__ == '__main__':
    # Configura o servidor
    server = SimpleXMLRPCServer((HOST, PORT))
    print('RPChat ready to accept connections')

    # Registra as funções
    server.register_function(services.create_room, 'create_room')
    server.register_function(services.join_room, 'join_room')
    server.register_function(services.leave_room, 'leave_room')
    server.register_function(services.list_rooms, 'list_rooms')
    server.register_function(services.send_msg, 'send_msg')
    server.register_function(services.recv_msgs, 'recv_msgs')
    server.register_function(services.list_users, 'list_users')

    # Registrar o servidor da calculadora no binder
    binder = xmlrpc.client.ServerProxy(f'http://localhost:{PORT - 1}')
    binder.register_service('rpchat', PORT)

    # Mantém o servidor em execução
    server.serve_forever()