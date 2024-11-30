import xmlrpc.client
import sys


if __name__ == "__main__":
    binder = xmlrpc.client.ServerProxy(f'http://localhost:12345')
    rpchat_port = binder.lookup_procedure('rpchat')

    if rpchat_port is None:
        print("Serviço de calculadora não encontrado.")
        exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    rpchat = xmlrpc.client.ServerProxy(f'http://localhost:{rpchat_port}')
    rpchat.create_room('babolei')
    token = rpchat.join_room('babolei', 'jacan')
    print(token)
    rpchat.leave_room(token)
