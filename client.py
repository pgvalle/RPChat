import xmlrpc.client

# binder = xmlrpc.client.ServerProxy(f'http://localhost:1234')
# host, port = binder.find_service('rpchat')

# if host == None or port == None:
#     print('This service was not registered')
#     exit(1)

# rpchat = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('RPChat Client')

style = ttk.Style(root)

def login_or_register_screen():
    # User and password entry
    top_frame = ttk.Frame(root)
    top_frame.grid(column=0, row=0)

    user_label = ttk.Label(top_frame, text='username:')
    user_label.grid(column=0, row=0)

    user_entry = ttk.Entry(top_frame, width=20)
    user_entry.grid(column=1, row=0, padx=5, pady=5)

    pass_label = ttk.Label(top_frame, text='password:')
    pass_label.grid(column=0, row=1)

    pass_entry = ttk.Entry(top_frame, width=20)
    pass_entry.grid(column=1, row=1, padx=5, pady=5)

    # Buttons
    bot_frame = ttk.Frame(root)
    bot_frame.grid(column=0, row=1)

    def login():
        user = user_entry.get()
        passw = pass_entry.get()

    login_btn = ttk.Button(bot_frame, text='login', command=login)
    login_btn.grid(column=0, row=0, padx=5, pady=5)

    def register():
        user = user_entry.get()
        passw = pass_entry.get()

        popup = tk.Toplevel(root)
        popup.title('Popup Window')

    regis_btn = ttk.Button(bot_frame, text='register', command=register)
    regis_btn.grid(column=1, row=0, padx=5, pady=5)

    def unregister():
        user = user_entry.get()
        passw = pass_entry.get()

    unreg_btn = ttk.Button(bot_frame, text='unregister', command=unregister)
    unreg_btn.grid(column=2, row=0, padx=5, pady=5)


login_or_register_screen()
root.mainloop()

# def main():
#     binder = xmlrpc.client.ServerProxy(f'http://localhost:1234')
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