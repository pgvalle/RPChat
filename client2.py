import xmlrpc.client, time, os

# binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
# host, port = binder.find_service('rpchat')

# if host == None or port == None:
#     print('This service was not registered')
#     exit(1)

rpchat = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1444')

text = None

def input_thread():
    text = input()

def main_thread():
    USER = 'hello'
    PASS = 'hello'
    rpchat.create_user(USER, PASS)
    rpchat.join_room('world', USER, PASS)

    i = 1
    while True:
        print('sleeping')
        time.sleep(2)
        print('not sleeping')
        rpchat.send_message('world', USER, PASS, f'hello men {i}')
        i += 1

    rpchat.leave_room('hallo')


main_thread()