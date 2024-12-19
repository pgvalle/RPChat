from sys import stdout, stdin
import platform

_is_windows = platform.system() == 'Windows'

if _is_windows:
    # enable ascii sequences
    import msvcrt, ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
else:
    import termios, tty

def init():
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def getkey():
    if _is_windows and msvcrt.kbhit():
        ch = msvcrt.getch()
        return ch.decode()
    
    if not _is_windows:
        fd = stdin.fileno()
        flags = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, flags)
        return ch
        
    return ''

def terminate():
    if not _is_windows:
        fd = stdin.fileno()
        os.set_blocking(fd, False)

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
