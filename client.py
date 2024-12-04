import xmlrpc.client
import sys, time, threading

messages = []
# urwid
exit_evt = threading.Event()

def recv_msgs():
    while not exit_evt.is_set():
        start = time.ctime()

        

        delta = time.ctime() - start
        
        if delta < 2:
            time.sleep(2 - delta)


def main():
    if len(sys.argv) < 3:
        print('Expected host and port')
        return
    
    # cli arguments parsing
    try:
        binder_host, binder_port = sys.argv[1], int(sys.argv[2])
    except Exception as e:
        print(f'Error when parsing arguments: {e}')
        return

    binder = xmlrpc.client.ServerProxy(f'http://{binder_host}:{binder_port}')
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
