from sys import stdout, stdin
import platform

_is_windows = platform.system() == 'Windows'

if _is_windows:
    # enable ascii sequences
    import msvcrt, ctypes, time
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
else:
    import select

def init():
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def getkey(timeout=0.01):
    if _is_windows:
        time.sleep(timeout)
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            return ch.decode()
    else:
        if select.select([stdin], [], [], 0.0)[0]:
            return stdin.read(1)
    
    return ''

def terminate():
    stdout.write('\x1b[?47l\x1b[?1049l')
    stdout.flush()
    exit(0)

def clear():
    stdout.write('\x1bc')
    stdout.flush()

def notify(text, timestamp=2):
    stdout.write(f'\n{text}')
    stdout.flush()

    import time
    time.sleep(timestamp)

    clear()
