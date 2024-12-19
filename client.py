import xmlrpc.client, sys
import tui, getpass

rpchat = None
username, password = '', ''
roomname = ''
users, messages = [], []

def get_option(options):
    opt = tui.getkey().lower()
    while not opt in options:
        opt = tui.getkey().lower()
    
    return opt

def get_credentials():
    username = input('username: ')
    if username == '':
        return None, None

    password = getpass.getpass('password: ')
    return username, password

def handle_screen_options(title, prompt, options):
    tui.clear()
    print('RPChat - ' + title)

    print(prompt, end='', flush=True)
    opt = get_option(options.keys())

    screen = options[opt]
    return screen, opt

def user_options_screen():
    OPTIONS = {
        'c': user_creation_screen,
        'd': user_deletion_screen,
        'l': user_login_screen,
        'q': lambda: None }
    PROMPT = '(c)reate user, (d)elete user, (l)ogin or (q)uit: '
    
    screen, opt = handle_screen_options('User Options', PROMPT, OPTIONS)
    return screen

def user_login_screen():
    tui.clear()
    print('RPChat - User login')

    global username, password
    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = None
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

    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = None
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

    username, password = get_credentials()
    if not username:
        return user_options_screen

    try:
        result = None
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
        'j': room_join_screen,
        'l': user_options_screen,
        'q': lambda: None }
    PROMPT = f'logged as {username}\n'
    PROMPT += '(c)reate room, (j)oin room or (l)ogout: '

    screen, opt = handle_screen_options('Room Screen', PROMPT, OPTIONS)
    return screen

def room_creation_screen():
    tui.clear()
    print('RPChat - Create Room')

    global roomname
    roomname = input('roomname: ')
    if roomname == '':
        return room_options_screen

    try:
        result = None
        result = rpchat.create_room(roomname)
    except Exception as e:
        tui.notify(f'Error: {e}')
        return room_options_screen

    if result == 0:
        print('join? [y/n]: ', end='', flush=True)
        opt = get_option(['y', 'n', 'yes', 'no'])

        if opt in ['y', 'yes']:
            return room_join_screen
    else:
        tui.notify(f'Error {result}')

    return room_options_screen

def room_join_screen():
    tui.clear()
    print('RPChat - Join Room')

    global roomname
    if roomname == '':
        roomname = input('roomname: ')
        if roomname == '':
            return room_options_screen
    else:
        print(f'roomname: {roomname}')
    
    try:
        result = None
        result = rpchat.join_room(roomname, username, password)
    except Exception as e:
        tui.notify(f'Error: {e}')
        return user_options_screen

    if isinstance(result, int):
        tui.notify(f'Error {result}')
        return room_options_screen

    global users, messages
    users, messages = result
    return room_screen

def room_screen():
    tui.clear()
    global roomname
    print(f'RPChat - {roomname}')

    import threading, time
    evt = threading.Event()
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def get_messages():
        global messages
        while not evt.is_set():
            with lock2:
                messages += rpchat.receive_messages(roomname, username, password)

            with lock1:
                print('\x1b[3;1H\x1b[J', end='')
                for date, orig, content, dest in messages:
                    print(f'[{date}][{orig}]: {content}')
                print('\x1b[2;1H', end='', flush=True)

            time.sleep(1)
    
    th = threading.Thread(target=get_messages, daemon=True)
    th.start()

    buffer = ''
    while not evt.is_set():
        a = ''
        with lock1:
            print('\x1b[1;1H', end='')
            print(f'RPChat - {roomname}', flush=True)
            print('\x1b[2;1H\x1b[K', end='')
            print(buffer, end='', flush=True)
        
        a = tui.getkey()
        if a == '\n' or a == '\r':
            with lock2:
                rpchat.send_message(roomname, username, password, buffer)
            buffer = ''
        elif a == '\r':
            buffer += a
        else:
            buffer += a

    evt.set()
    th.join()

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
        print(f'Error connecting to rpchat: {e}')
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
