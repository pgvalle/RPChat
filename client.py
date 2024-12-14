import xmlrpc.client

binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
host, port = binder.find_service('rpchat')

if host == None or port == None:
    print('This service was not registered')
    exit(1)

rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

root = tk.Tk()
root.title('RPChat Client')
root.resizable(False, False)

style = ttk.Style(root)

rooms_windows = []
username, password = tk.StringVar(), tk.StringVar()


def room_window(roomname):
    room_root = tk.Toplevel(root)
    room_root.title(f'{roomname}')
    room_root.resizable(False, False)

    rooms_windows.append(room_root)

    screen = ttk.Frame(room_root)
    screen.pack(fill='both')


def user_screen():
    screen = ttk.Frame(root)
    screen.pack(fill='both')

    #### Screen

    # screen widgets
    user_frame = ttk.Frame(screen)
    rooms_listbox = tk.Listbox(screen)
    room_frame = ttk.Frame(screen)
    room_actions_frame = ttk.Frame(screen)

    # screen widgets placement
    user_frame.grid(column=0, row=0)
    rooms_listbox.grid(column=0, row=1, sticky='snew', padx=5, pady=5)
    room_frame.grid(column=0, row=2)
    room_actions_frame.grid(column=0, row=3)

    #### User Frame

    # widgets inside userframe

    def logout():
        screen.destroy()
        for room_window in rooms_windows:
            room_window.destroy()

        main_screen()

    login_label = ttk.Label(user_frame, text=f'Logged as {username.get()}')
    logout_btn = ttk.Button(user_frame, text='logout', command=logout)

    # positioning widgets inside userframe
    login_label.grid(column=0, row=0, padx=5, pady=5)
    logout_btn.grid(column=1, row=0, padx=5, pady=5)

    #### Room Frame

    # widgets inside room_frame
    room_label = ttk.Label(room_frame, text='roomname:')
    room_entry = ttk.Entry(room_frame)

    # placing user input widgets in room_frame
    room_label.grid(column=0, row=0)
    room_entry.grid(column=1, row=0)

    #### Room actions frame

    # actions inside room actions frame

    def refresh_list():
        rooms = rpchat.list_rooms()
        i = rooms.index('world')
        
        rooms_listbox.delete(0)
        rooms_listbox.insert(0, rooms)
        rooms_listbox.select_set(i)

    def join_room():
        roomname = room_entry.get()
        result = rpchat.join_room(roomname, username.get(), password.get())

        if isinstance(result, int):
            msgbox.showerror(message=f'Error {result}')
        else:
            room_window(roomname)


    create_btn = ttk.Button(room_actions_frame, text='create', command=None)
    join_btn = ttk.Button(room_actions_frame, text='join', command=join_room)
    refresh_list_btn = ttk.Button(room_actions_frame, text='refresh list', command=refresh_list)

    # actions placement inside room actions frame
    create_btn.grid(column=0, row=0)
    join_btn.grid(column=1, row=0)
    refresh_list_btn.grid(column=2, row=0)


def main_screen():
    screen = ttk.Frame(root)
    screen.pack(fill='both', padx=4, pady=4)

    #### screen
    
    # Widgets
    inputs_frame = ttk.Frame(screen)
    actions_frame = ttk.Frame(screen)

    # Widgets placement in screen
    inputs_frame.grid(column=0, row=0)
    actions_frame.grid(column=0, row=1, sticky='snew')

    ### inputs frame

    # widgets inside inputs_frame
    user_label = ttk.Label(inputs_frame, text='username:')
    user_entry = ttk.Entry(inputs_frame, textvariable=username)
    pass_label = ttk.Label(inputs_frame, text='password:')
    pass_entry = ttk.Entry(inputs_frame, show='*', textvariable=password)
    
    # placing user input widgets in inputs frame
    user_label.grid(column=0, row=0)
    user_entry.grid(column=1, row=0, padx=4, pady=4)
    pass_label.grid(column=0, row=1)
    pass_entry.grid(column=1, row=1, padx=4, pady=4)

    ### actions frame
    
    # actions in actions frame

    def login():
        result = rpchat.check(username.get(), password.get())

        if result == 0:
            screen.destroy()
            user_screen()
        else:
            msgbox.showerror(message=f'Error {result}')

    def register():
        result = rpchat.register_user(username.get(), password.get())

        if result == 0:
            # reset fields
            username.set('')
            password.set('')
            msgbox.showinfo(message=f'User {username.get()} registered successfully')
        else:
            msgbox.showerror(message=f'Error {result}')

    def unregister():
        result = rpchat.unregister_user(username.get(), password.get())

        if result == 0:
            username.set('')
            password.set('')
            msgbox.showinfo(message=f'User {username.get()} unregistered successfully')
        else:
            msgbox.showerror(message=f'Error {result}')

    login_btn = ttk.Button(actions_frame, text='login', command=login)
    regis_btn = ttk.Button(actions_frame, text='register', command=register)
    unreg_btn = ttk.Button(actions_frame, text='unregister', command=unregister)

    # positioning actions in actions frame
    login_btn.grid(column=0, row=0, padx=5, pady=5)
    regis_btn.grid(column=1, row=0, padx=5, pady=5)
    unreg_btn.grid(column=2, row=0, padx=5, pady=5)


main_screen()
root.mainloop()

# def main():
#     binder = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1234')
#     host, port = binder.find_service('rpchat')

#     if [host, port] == [None, None]:
#         print('This service was not registered')
#         exit(1)

#     # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
#     rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')
#     rpchat.create_room('adam')
#     rpchat.register_user('adam', '123')
#     tk = rpchat.login('adam', '123')
#     print(tk)

#     rpchat.join_room('world', 'adam', tk)

# main()