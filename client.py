import xmlrpc.client, curses

binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
host, port = binder.find_service('rpchat')

if host == None or port == None:
    print('This service was not registered')
    exit(1)

rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')