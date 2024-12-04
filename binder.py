from xmlrpc.server import SimpleXMLRPCServer
import sys

services = {}

def register_service(name, host, port):
    services[name] = (host, port)
    print(f'Service {name} registered at {host}:{port}')
    return True

def unregister_service(name):
    if name in services:
        del services[name]

def find_service(name):
    return services.get(name, None)

def main():
    if len(sys.argv) < 3:
        print('Expected host and port')
        return
    
    # cli arguments parsing
    try:
        host, port = sys.argv[1], int(sys.argv[2])
    except Exception as e:
        print(f'Error when parsing arguments: {e}')
        return

    # Create XML-RPC server for binder
    try:
        binder_server = SimpleXMLRPCServer((host, port), logRequests=False)
    except Exception as e:
        print(f'Error when creating server: {e}')
        return

    # register functions
    binder_server.register_function(register_service, 'register_service')
    binder_server.register_function(unregister_service, 'unregister_service')
    binder_server.register_function(find_service, 'find_service')

    print(f'Binder ready at {host}:{port}')

    # keep binder running
    try:
        binder_server.serve_forever()
    except KeyboardInterrupt:
        print('bye')

    binder_server.server_close()


if __name__ == '__main__':
    main()
