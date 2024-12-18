import xmlrpc.client
import cli

rpchat = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1444')

def main_screen():
    SCREEN_FROM_ACTION = {
        'c': create_user_screen,
        'l': lambda: print('not done yet') }

    PROMPT = '(c)reate new user, (l)ogin or press ctrl+c twice to quit: '

    while True:
        cli.clear()
        act = input(PROMPT).lower()
    
        while not act in SCREEN_FROM_ACTION.keys():
            cli.notify('Invalid action', stamp=1)
            act = input(PROMPT).lower()
        
        screen = SCREEN_FROM_ACTION[act]
        cli.execute(screen)

def create_user_screen():
    while True:
        cli.clear()
        print('User creation')
        result = create_user()
        if result == 0:
            break

def create_user():
    try:
        username, password = get_credentials()
        return rpchat.create_user(username, password)
    except:
        return -10
    
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