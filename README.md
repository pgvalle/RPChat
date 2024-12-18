# Objetivo do Trabalho

Implementar um sistema de chat distribuído com múltiplas salas, utilizando RPC
(Remote Procedure Call) em Python. O sistema deve incluir um servidor que
gerencie salas de chat e múltiplos clientes que podem criar salas, entrar em
salas existentes e interagir por meio de mensagens públicas (broadcast) e
privadas (unicast). Cada usuário deve possuir um username único, e o servidor
deve garantir que nomes duplicados não sejam permitidos.

Adicionalmente, o aluno deve implementar um binder centralizado, que será
responsável por gerenciar as portas e endereços dos procedimentos remotos
disponíveis no servidor, permitindo o registro e descoberta dos métodos RPC.
O trabalho deve estar organizado em diretórios, não entregar tudo em um único
arquivo .py.

