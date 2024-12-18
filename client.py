import xmlrpc.client

# binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
# host, port = binder.find_service('rpchat')
# rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')
binder =None
host, port = None, None
rpchat = None
import tui, getpass

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
        'l': user_login_screen,
        'q': lambda: None }
    PROMPT = '(c)reate user, (l)ogin or (q)uit: '
    
    screen = handle_options('User Options', PROMPT, OPTIONS)
    return screen

def user_login_screen():
    tui.clear()
    print('RPChat - User login')

    global username, password
    username, password = get_credentials()
    if not username:
        return user_options_screen

    result = 0

    try:
        result = rpchat.check_user(username, password)        
    except Exception as e:
        tui.notify(f'Error: {e}')

    if result == 0:
        return room_options_screen()
    else:
        tui.notify(f'Error {result}')

    return user_options_screen

def user_creation_screen():
    tui.clear()
    print('RPChat - User creation')

    result = 0
    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = rpchat.create_user(username, password)
    except Exception as e:
        tui.notify(f'Error: {e}')

    if result == 0:
        tui.notify(f'user {username} created')
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
    PROMPT = f'logged as {username}'
    PROMPT += '(c)reate room, (j)oin room, (s)earch room or (l)ogout: '

    screen = handle_options('Room Screen', PROMPT, OPTIONS)
    return screen

def room_creation_screen():
    tui.clear()
    print('RPChat - Room creation')

    result = 0
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

def main():
    tui.init()

    try:
        screen_function = user_options_screen
        while screen_function:
            screen_function = screen_function()
    except KeyboardInterrupt:
        pass

    tui.terminate()

main()
