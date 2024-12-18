from sys import stdout, stdin
import platform

_is_windows = platform.system() == 'Windows'

if _is_windows:
    import msvcrt
else:
    import fcntl

def init():
    if _is_windows:
        import ctypes
        # enable ascii sequences
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        import os
        # unblock stdin
        fd = stdin.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def getkey():
    if _is_windows:
        if msvcrt.kbhit():  # Check if input is available
            return msvcrt.getch().decode()  # Return single character
    else:
        try:
            return stdin.read()  # Read available input
        except IOError:
            pass
    
    return None

def terminate():
    stdout.write('\x1b[?47l\x1b[?1049l')
    stdout.flush()
    exit(0)

def clear():
    stdout.write('\x1bc')
    stdout.flush()

def notify(text, timestamp=2):
    clear()
    print(text)
    import time
    time.sleep(timestamp)    
    clear()
