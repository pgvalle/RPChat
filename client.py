import xmlrpc.client

binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
host, port = binder.find_service('rpchat')
rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

import cli, getpass, sys, selectors

selector = selectors.DefaultSelector()
selector.register(sys.stdin, selectors.EVENT_READ)

username, password = '', ''

def handle_options(title, prompt, options):
    cli.clear()
    print(title)

    print(prompt)
    opt = cli.getkey()

    while not opt in options:
        cli.notify('Invalid option')
        print(prompt)
        opt = cli.getkey()
        print(opt)

    screen = options[opt]
    return screen

def user_options_screen():
    OPTIONS = {
        'c': user_creation_screen,
        'l': user_login_screen,
        'q': lambda: None }
    PROMPT = '(c)reate user, (l)ogin or (q)uit: '
    
    screen = handle_options('RPChat', PROMPT, OPTIONS)
    return screen

def user_login_screen():
    cli.clear()
    print('User login')

    global username, password
    username, password = '', ''

    username = input('username: ')
    if username == '':
        return user_options_screen
    
    password = getpass.getpass('password: ')

    try:
        result = rpchat.check_user(username, password)        
    except OSError as e:
        cli.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        cli.notify(f'RPC Error: {e}')

    if result == 0:
        return room_options_screen()
    else:
        cli.notify(f'Error {result}')

    return user_options_screen

def user_creation_screen():
    cli.clear()
    print('User creation')
    
    username = input('username: ')
    if username == '':
        return user_options_screen

    password = getpass.getpass('password: ')

    try:
        result = rpchat.create_user(username, password)
    except OSError as e:
        cli.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        cli.notify(f'RPC Error: {e}')

    if result == 0:
        cli.notify(f'user {username} created')
    else:
        cli.notify(f'Error {result}')

    return user_options_screen

def room_options_screen():
    OPTIONS = {
        'c': room_creation_screen,
        'j': room_screen,
        's': room_search_screen,
        'l': user_options_screen,
        'q': lambda: None }
    PROMPT = f'logged as {username}'
    PROMPT += '(c)reate room, (j)oin room, (s)earch room or (l)ogout: '

    screen = handle_options('Room Screen', PROMPT, OPTIONS)
    return screen

def room_creation_screen():
    cli.clear()
    print('Room creation')

    roomname = input('roomname: ')
    if roomname == '':
        return room_screen

    try:
        result = rpchat.create_room(roomname)
    except OSError as e:
        cli.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        cli.notify(f'RPC Error: {e}')

    if result == 0:
        cli.notify('room {roomname} created')
    else:
        cli.notify(f'Error {result}')

    return room_screen

def room_search_screen():
    cli.clear()
    print('Room search')
    
    try:
        rooms = rpchat.list_rooms()
    except OSError as e:
        cli.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        cli.notify(f'RPC Error: {e}')

    for room in rooms:
        print(room)
    
    input('press enter to go back')
    return room_options_screen

def room_screen():
    pass

def main():
    cli.init()

    screen_function = user_options_screen
    while screen_function:
        screen_function = screen_function()

    cli.terminate()

while True:
    a=cli.getkey()
    print(a)
main()