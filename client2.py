import xmlrpc.client
from sys import stdout, stdin

rpchat = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1444')

def enable_vt100_on_windows():
    '''Enable VT100 mode in Windows cmd if necessary.'''
    import platform

    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except (ImportError, AttributeError):
            pass

def clear_screen():
    stdout.write('\x1bc')
    stdout.flush()

def main_screen():
    ACTIONS = {
        'c': create_user_screen,
        'l': 1,
        'q': lambda: exit(0) }

    while True:
        try:
            clear_screen()
            act = input('(c)reate new user, (l)ogin or (q)uit: ').lower()
            while not act in ACTIONS:
                clear_screen()
                print('Invalid action')
                act = input('(c)reate new user, (l)ogin or (q)uit: ')
            return ACTIONS[act]
        except KeyboardInterrupt:
            pass

    

def create_user_screen():
    while True:
        try:
            clear_screen()
            print(f'Create username')
            return get_credentials()
        except KeyboardInterrupt:
            pass

def create_user(username, password):
    try:
        return rpchat.create_user(username, password)
    except:
        return None
    
def get_credentials():
    username = input('username: ')
    password = input('password: ')
    return username, password



def main():
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

    

    stdout.write('\x1b[?47l\x1b[?1049l')
    stdout.flush()

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

enable_vt100_on_windows()
main()