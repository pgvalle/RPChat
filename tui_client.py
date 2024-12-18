import time
from blessed import Terminal
import time

term = Terminal()

if __name__ == "__main__":
    with term.fullscreen(), term.cbreak():
        print(term.black_on_yellow('hello') + term.normal)

        time.sleep(2)