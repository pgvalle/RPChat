import xmlrpc.client
import cli

rpchat = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')

def main_screen():
    SCREEN_FROM_ACTION = {
        'c': user_creation_screen,
        'l': user_login_screen }

    PROMPT = '(c)reate new user, (l)ogin or press ctrl+c twice to quit: '

    while True:
        cli.clear()
        act = input(PROMPT).lower()
    
        while not act in SCREEN_FROM_ACTION.keys():
            cli.notify('Invalid action', stamp=1)
            act = input(PROMPT).lower()
        
        screen = SCREEN_FROM_ACTION[act]
        cli.execute(screen, time_to_compute_quit=0.5)

def user_login_screen():
    while True:
        cli.clear()
        print('User login')
        try:
            username, password = get_credentials()
            result = rpchat.check(username, password)
            if result == 0: break
            else: cli.notify(f'Error {result}')
        except OSError as e:
            cli.notify(f'OS Error: {e}')
        except xmlrpc.client.Fault as e:
            cli.notify(f'RPC Error: {e}')

def user_creation_screen():
    while True:
        cli.clear()
        print('User creation')
        try:
            username, password = get_credentials()
            result = rpchat.create_user(username, password)
            if result == 0: break
            else: cli.notify(f'Error {result}')
        except OSError as e:
            cli.notify(f'OS Error: {e}')
        except xmlrpc.client.Fault as e:
            cli.notify(f'RPC Error: {e}')
    
def get_credentials():
    username = input('username: ')
    password = input('password: ')
    return username, password



def main():
    cli.init()

    main_screen()

    cli.terminate()

    # USER = 'hello'
    # PASS = 'hello'
    # rpchat.create_user(USER, PASS)
    # rpchat.join_room('world', USER, PASS)

    # i = 1
    # while True:
    #     print('sleeping')
    #     time.sleep(2)
    #     print('not sleeping')
    #     rpchat.send_message('world', USER, PASS, f'hello men {i}')
    #     i += 1


    # rpchat.leave_room('hallo')

cli.execute(main)
cli.terminate()