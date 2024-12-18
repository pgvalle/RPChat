from sys import stdout, stdin
import platform

_is_windows = platform.system() == 'Windows'
_selector = None

if _is_windows:
    # enable ascii sequences
    import msvcrt, ctypes, time
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
else:
    import selectors
    _selector = selectors.DefaultSelector()
    _selector.register(stdin, selectors.EVENT_READ)

def init():
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def printil(text):
    stdout.write(text)
    stdout.flush()

def getkey(timeout=0.01):
    if _is_windows:
        time.sleep(timeout)
        ch = msvcrt.getch()
        return ch.decode() if ch else ''
    
    global selector
    events = _selector.select(timeout)
    result = ''
    for key, _ in events:
        if key.fileobj == stdin:
            result += str(key.data)
    return result

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
