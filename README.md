# Como Executar o sistema

Tem 3 arquivos que devem ser executados: binder.py, server.py e client.py

O servidor recebe o host em que vai servir, o host do binder e a porta do binder\
```python server.py localhost localhost 12345```

O Binder recebe host e porta em que vai servir\
```python binder.py localhost 12345```

O cliente recebe host e porta com os quais vai se conectar\
```python client.py localhost 12345```

Árvore do diretório raiz
```
.
├── binder.py
├── client.py
├── guiclient.py
├── LICENSE
├── README.md
├── requirements.txt
├── server.py
├── srv
│   ├── entities.py
│   ├── functions.py
│   ├── main.py
│   └── statcodes.py
└── tui.py
```

Os métodos rpc são registrados no servidor e no binder é registrado o serviço com nome rpchat, acessado no cliente