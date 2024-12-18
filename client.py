import xmlrpc.client, sys
import tui, getpass

rpchat = None
username, password = '', ''

def handle_options(title, prompt, options):
    tui.clear()
    print('RPChat - ' + title)

    print(prompt, end='', flush=True)
    opt = tui.getkey().lower()

    while not opt in options.keys():
        opt = tui.getkey().lower()

    screen = options[opt]
    return screen

def get_credentials():
    username = input('username: ')
    if username == '':
        return None, None

    password = getpass.getpass('password: ')
    return username, password

def user_options_screen():
    OPTIONS = {
        'c': user_creation_screen,
        'd': user_deletion_screen,
        'l': user_login_screen,
        'q': lambda: None }
    PROMPT = '(c)reate user, (d)elete user, (l)ogin or (q)uit: '
    
    screen = handle_options('User Options', PROMPT, OPTIONS)
    return screen

def user_login_screen():
    tui.clear()
    print('RPChat - User login')

    global username, password
    username, password = get_credentials()
    if not username:
        return user_options_screen

    result = None

    try:
        result = rpchat.check_user(username, password)        
    except Exception as e:
        tui.notify(f'Error: {e}')
        return user_options_screen

    if result == 0:
        return room_options_screen
    else:
        tui.notify(f'Error {result}')

    return user_options_screen

def user_creation_screen():
    tui.clear()
    print('RPChat - Create user')

    result = None
    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = rpchat.create_user(username, password)
    except Exception as e:
        tui.notify(f'Error: {e}')
        return user_options_screen 

    if result == 0:
        tui.notify(f'user {username} created')
    else:
        tui.notify(f'Error {result}')

    return user_options_screen

def user_deletion_screen():
    tui.clear()
    print('RPChat - Delete user')

    result = None
    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = rpchat.delete_user(username, password)
    except Exception as e:
        tui.notify(f'Error: {e}')
        return user_options_screen 

    if result == 0:
        tui.notify(f'user {username} deleted')
    else:
        tui.notify(f'Error {result}')

    return user_options_screen

def room_options_screen():
    OPTIONS = {
        'c': room_creation_screen,
        'j': room_screen,
        's': room_search_screen,
        'l': user_options_screen,
        'q': lambda: None }
    PROMPT = f'logged as {username}\n'
    PROMPT += '(c)reate room, (j)oin room, (s)earch room or (l)ogout: '

    screen = handle_options('Room Screen', PROMPT, OPTIONS)
    return screen

def room_creation_screen():
    tui.clear()
    print('RPChat - Room creation')

    result = None
    roomname = input('roomname: ')
    if roomname == '':
        return room_screen

    try:
        result = rpchat.create_room(roomname)
    except OSError as e:
        tui.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        tui.notify(f'RPC Error: {e}')

    if result == 0:
        tui.notify('room {roomname} created')
    else:
        tui.notify(f'Error {result}')

    return room_screen

def room_search_screen():
    tui.clear()
    print('RPChat - Room search')
    
    try:
        rooms = rpchat.list_rooms()
    except OSError as e:
        tui.notify(f'OS Error: {e}')
    except xmlrpc.client.Fault as e:
        tui.notify(f'RPC Error: {e}')

    for room in rooms:
        print(room)
    
    input('press enter to go back')
    return room_options_screen

def room_screen():
    pass

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
    binder_addr = parse_cli_args()

    try:
        binder = xmlrpc.client.ServerProxy(f'http://{binder_addr[0]}:{binder_addr[1]}')
        server_addr = binder.find_service('rpchat')

        global rpchat
        rpchat = xmlrpc.client.ServerProxy(f'http://{server_addr[0]}:{server_addr[1]}')
    except Exception as e:
        print(f'Error connecting to binder: {e}')
        exit(3)

    tui.init()

    try:
        screen_function = user_options_screen
        while screen_function:
            screen_function = screen_function()
    except KeyboardInterrupt:
        pass

    tui.terminate()

main()
