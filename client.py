import xmlrpc.client

def main():
    binder = xmlrpc.client.ServerProxy(f'http://localhost:1234')
    host, port = binder.find_service('rpchat')

    if [host, port] == [None, None]:
        print('This service was not registered')
        exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')
    rpchat.create_room('adam')
    rpchat.register_user('adam', '123')
    tk = rpchat.login('adam', '123')
    print(tk)

    rpchat.join_room('world', 'adam', tk)

main()