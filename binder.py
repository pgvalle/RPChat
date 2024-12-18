from xmlrpc.server import SimpleXMLRPCServer
import sys

services = {}

def register_service(name, host, port):
    services[name] = (host, port)
    print(f'registered service {name} at {host, port}')
    return True

def find_service(name):
    return services.get(name, None)

def parse_cli_args():
    if len(sys.argv) < 3:
        print('Expected host and port')
        exit(1)
    
    try:
        addr = sys.argv[1], int(sys.argv[2])
        return addr
    except Exception as e:
        print(f'Error parsing arguments: {e}')
        exit(2)

def main():
    addr = parse_cli_args()

    try:
        binder_server = SimpleXMLRPCServer(addr, logRequests=False, allow_none=True)
    except Exception as e:
        print(f'Error creating binder server: {e}')
        exit(2)

    binder_server.register_function(register_service, 'register_service')
    binder_server.register_function(find_service, 'find_service')

    print(f'Binder ready at {addr}')

    try:
        binder_server.serve_forever()
    except KeyboardInterrupt:
        print('bye')
    finally:
        binder_server.server_close()


if __name__ == '__main__':
    main()
