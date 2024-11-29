from random import choices

__TOKEN_CHARS = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?@#$%&*')

def create_token(size):
    token_as_list = choices(__TOKEN_CHARS, k=size)
    return ''.join(token_as_list)