from . import statcodes, config
import datetime


class Room:

    def __init__(self, name):
        self.name = name
        self.users = {}
        self.messages = []
        self.time_inactive = 0

        self.log('I was just created')

    def log(self, msg):
        print(f'{self.name}: {msg}')
    
    def join(self, username):
        if username in self.users:
            self.log(f'someone tried to join as {username}')
            return statcodes.USER_EXISTS

        self.users[username] = datetime.datetime(1978, 1, 1)
        self.log(f'{username} joined')

        i = len(self.messages) - 1
        messages = []

        while i >= 0 and len(self.messages) - i <= 50:
            orig, dest, content, date = self.messages[i]

            if not dest:
                messages.insert(0, (orig, content, date))
            
            i -= 1

        return self.users, messages

    def send_msg(self, username, msg, recipient=None):
        if not username in self.users:
            self.log(f'{username} is not in the room and tried to send a message')
            return statcodes.USER_NOT_FOUND

        self.messages.append((
            username, # origin
            recipient, # destination
            msg, # content
            datetime.datetime.now() # date
        ))

        if recipient == username:
            self.log(f'{username} messaged themselves')
        elif recipient:
            self.log(f'{username} messaged {recipient}')
        else:
            self.log(f'{username} messaged everyone')

        return statcodes.SUCCESS

    def recv_msgs(self, username):
        if not username in self.users:
            return statcodes.USER_NOT_FOUND

        i = len(self.messages) - 1
        messages = []
        last_date =  self.users[username]

        while i >= 0:
            _, dest, _, date = self.messages[i]

            if date < last_date:
                break

            if not dest or dest == username:
                messages.insert(0, self.messages[i])
            
            i -= 1

        self.users[username] = datetime.datetime.now()

        return messages
