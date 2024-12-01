import xmlrpc.client
import sys


if __name__ == '__main__':
    binder = xmlrpc.client.ServerProxy(f'http://localhost:1234')
    host, port = binder.lookup_procedure('rpchat')

    if [host, port] == [None, None]:
        print('This service was not registered')
        exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')
    rpchat.create_room('babolei')
    result = rpchat.join_room('babolei', 'jacan')
    print(result)
    rpchat.leave_room('babolei', result[0])
