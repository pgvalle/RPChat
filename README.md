# Objetivo do Trabalho

Implementar um sistema de chat distribuído com múltiplas salas, utilizando RPC
(Remote Procedure Call) em Python. O sistema deve incluir um servidor que gerencie
salas de chat e múltiplos clientes que podem criar salas, entrar em salas
existentes e interagir por meio de mensagens públicas (broadcast) e privadas (unicast).
Cada usuário deve possuir um username único, e o servidor deve garantir que nomes
duplicados não sejam permitidos.

Adicionalmente, o aluno deve implementar um binder centralizado, que será responsável
por gerenciar as portas e endereços dos procedimentos remotos disponíveis no
servidor, permitindo o registro e descoberta dos métodos RPC. O trabalho deve estar
organizado em diretórios, não entregar tudo em um único arquivo .py.


# Regras e Especificações do Sistema

## Binder

### Gerenciamento dos Procedimentos Remotos

* O binder deve ser um componente central responsável por registrar todas as
  portas e endereços dos procedimentos remotos disponíveis no servidor.
  Ele deve oferecer os seguintes métodos via RPC:

    * `register_procedure(procedure_name, address, port)`
      ```
      Permite que o servidor registre os métodos RPC disponíveis, associando-os a um
      nome, endereço IP e porta.
      ```
    * `lookup_procedure(procedure_name)`
      ```
      Permite que os clientes descubram o endereço e a porta de um procedimento remoto pelo nome.
      ```

### Funcionamento do Binder

* Deve ser executado em uma porta fixa conhecida por todos (ex.: 5000).
* Todos os métodos RPC do servidor devem ser registrados no binder.


## Servidor (RPC Server)

### Gerenciamentode Usuários

* Cada usuário deve se registrar com um username único.
* O servidor deve rejeitar conexões de usuários que tentem utilizar um nome já em uso.

### Gerenciamento de Salas

* O servidor deve gerenciar múltiplas salas de chat, cada uma com um nome único
  e uma lista de mensagens (histórico).
* O servidor deve ter manter uma lista de usuários conectados na sala
* O histório de cada sala deve incluir:
    * tipo da mensagem (broadcast ou unicast)
    * usuário origem 
    * usuário destino (no caso de unicast).
    * conteúdo da mensagem
    * data e hora em que a mensagem foi enviada

### Funcionalidades Disponíveis (Registradas no Binder):

* `create_room(room_name)`
  ```
  Cria uma nova sala com o nome fornecido. O servidor deve garantir que o nome
  da sala seja único.
  ```
* `join_room(username, room_name)`
  ```
  Permite que o usuário entre em uma sala existente. Anuncia a entrada do
  usuário para todos.
  Retorna A lista de usuários conectados na sala e as últimas 50 mensagens
  públicas (broadcast) da sala.
  ```
* `send_message(username, room_name, message, recipient=None)`
  ```
  Envia uma mensagem pública se recipient=None. Caso contrário, a mensagem é
  enviada apenas para o destinatário especificado.
  ```
* `receive_messages(username, room_name)`
  ```
  Retorna todas as mensagens públicas e privadas com recipient=username enviadas
  para a sala desde a última busca do usuário.
  ```
* `list_rooms()`
  ```
  Retorna a lista de salas disponíveis no servidor.
  ```
* `list_users(room_name)`
  ```
  Retorna a lista de usuários conectados em uma sala específica.
  ```

### Remoção de Usuários e Salas

* Quando um usuário sai de uma sala, ele deve ser removido da lista de usuários conectados.
* Salas sem usuários conectados podem ser automaticamente removidas após 5 minutos de inatividade.


## Cliente

### Registro de usuário

* O cliente deve permitir que o usuário registre-se com um username único.
* Caso o nome já esteja em uso, o cliente deve exibir uma mensagem de erro e
solicitar outro nome.

### Interação com o sistema

O cliente deve permitir:

Criar uma sala: Solicita ao servidor a criação de uma sala com um nome único.
Entrar em uma sala: Permite entrar em uma sala existente e exibe a lista de
usuários conectados e as últimas 50 mensagens públicas