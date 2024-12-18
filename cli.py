from sys import stdout

def init():
    import platform
    if platform.system() == 'Windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except (ImportError, AttributeError): pass
    
    stdout.write('\x1b[?1049h\x1b[?47h')
    stdout.flush()

def terminate():
    clear()
    stdout.write('\x1b[?47l\x1b[?1049l')
    stdout.flush()
    exit(0)

screens = {}

def register_screen(screen, key):
    screens[key] = screen

def clear():
    stdout.write('\x1bc')
    stdout.flush()

def notify(text, timestamp=2):
    def _notify():
        stdout.write(text)
        stdout.flush()
        import time
        time.sleep(timestamp)
    
    clear()
    execute(_notify, time_to_compute_quit=None)
    clear()

def execute(function, time_to_compute_quit=None):
    # one KeyboardInterrupt goes back to previous function
    try:
        screen = screens[None]
        screen()
    except KeyboardInterrupt: pass
    
    # two KeyboardInterrupts within time range quit the app
    if time_to_compute_quit:
        try:
            import time
            time.sleep(time_to_compute_quit)
        except KeyboardInterrupt: terminate()