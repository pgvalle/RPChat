import xmlrpc.client, time, os

rpchat = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1444')

text = None

def input_thread():
    text = input()

def main_thread():
    USER = 'hallo'
    PASS = 'hallo'
    rpchat.create_user(USER, PASS)
    print('here')
    rpchat.join_room('world', USER, PASS)
    print('here')
    while True:
        print('sleeping')
        time.sleep(2)
        os.system('cls')
        print('not sleeping')
        msgs = rpchat.receive_messages('world', USER, PASS)
        print('here')
        for msg in msgs:
            print(msg)


main_thread()