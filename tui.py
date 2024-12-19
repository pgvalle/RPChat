from sys import stdout, stdin
import platform

_is_windows = platform.system() == 'Windows'
_stdin_fd = stdin.fileno()

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
        flags = termios.tcgetattr(_stdin_fd)
        try:
            tty.setcbreak(_stdin_fd)
            ch = stdin.read(1)
        finally:
            termios.tcsetattr(_stdin_fd, termios.TCSADRAIN, flags)
        return ch
        
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
