from xmlrpc.server import SimpleXMLRPCServer
import rpchat
import sys


services_registry = {}


def register_procedure(servicename, host, port):
    services_registry[servicename] = (host, port)
    print(f'Service {servicename} registered at {host}:{port}')
    return True


def lookup_procedure(servicename):
    return services_registry.get(servicename, None)


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
    binder_server.register_function(register_procedure, 'register_procedure')
    binder_server.register_function(lookup_procedure, 'lookup_procedure')

    print(f'Binder ready at {host}:{port}')

    # keep binder running
    try:
        binder_server.serve_forever()
    except KeyboardInterrupt:
        print('bye')

    binder_server.server_close()


if __name__ == '__main__':
    main()