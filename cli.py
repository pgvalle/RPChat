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

def notify(text, timestamp=2):
    clear()
    print(text)

    try:
        import time
        time.sleep(timestamp)
    except KeyboardInterrupt:
        pass
    
    clear()

def run_screen(function, out_function):
    try:
        return function()
    except KeyboardInterrupt:
        pass
    
    return out_function
