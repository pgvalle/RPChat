import xmlrpc.client
import cli, getpass

binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
host, port = binder.find_service('rpchat')
rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

def main_screen():
    OPTIONS = {
        'c': user_creation_screen,
        'l': user_login_screen,
        'q': lambda: None }
    PROMPT = '(c)reate user, (l)ogin or (q)uit: '

    cli.clear()
    opt = input(PROMPT).lower()

    while not opt in OPTIONS:
        cli.notify('Invalid option')
        opt = input(PROMPT).lower()
    
    screen = OPTIONS[opt]
    return cli.run_screen(screen, main_screen)

def room_option_screen(username, password):
    OPTIONS = {
        'c': user_creation_screen,
        'j': user_login_screen,
        'l': main_screen }
    PROMPT = '(c)reate room, (j)oin room or (l)ogout: '

    input(PROMPT)

def user_login_screen():
    cli.clear()
    print('User login')

    username = input('username: ')
    password = getpass.getpass('password: ')

    try:
        result = rpchat.check_user(username, password)
        if result == 0:
            return lambda: room_option_screen(username, password)
        else:
            cli.notify(f'Error {result}')
    except (OSError, xmlrpc.client.Fault) as e:
        cli.notify(f'Error: {e}')

    return main_screen

def user_creation_screen():
    cli.clear()
    print('User creation')
    
    try:
        username = input('username: ')
        password = getpass.getpass('password: ')
        result = rpchat.create_user(username, password)

        if result == 0:
            cli.notify(f'user {username} created')
        else:
            cli.notify(f'Error {result}')
    except OSError as e:
        cli.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        cli.notify(f'RPC Error: {e}')

    return main_screen

def main():
    cli.init()

    screen_function = main_screen
    while screen_function:
        screen_function = cli.run_screen(main_screen, None)

    cli.terminate()

main()