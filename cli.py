from sys import stdout

def init():
    import platform
    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except (ImportError, AttributeError):
            pass
    
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def terminate():
    stdout.write('\x1b[?47l\x1b[?1049l')
    stdout.flush()
    exit(0)

def clear():
    stdout.write('\x1bc')
    stdout.flush()

def notify(text, stamp=2):
    import time

    clear()
    stdout.write(text)
    stdout.flush()
    time.sleep(stamp)
    clear()

def execute(screen):
    # one KeyboardInterrupt goes back to previous screen
    try: screen()
    except KeyboardInterrupt: pass
    
    # two KeyboardInterrupts within 0.5 seconds quit the app
    try: notify(text='', stamp=0.5)
    except KeyboardInterrupt: terminate()