from xmlrpc.server import SimpleXMLRPCServer
import config

# TODO Implement my own binder
# Dicionário para armazenar o serviço e a porta correspondente
services_registry = {}


# Função para registrar um serviço no binder
def register_procedure(servicename, port):
    services_registry[servicename] = port
    print(f'Service {servicename} registered in {port}')
    return True


# Função para descobrir a porta de um serviço
def lookup_procedure(servicename):
    return services_registry.get(servicename, None)


if __name__ == '__main__':
    # Cria o servidor XML-RPC para o binder
    binder_server = SimpleXMLRPCServer((config.HOST, config.PORT))
    print('Binder waiting for new registrations')

    # Registra as funções
    binder_server.register_function(register_procedure, 'register_procedure')
    binder_server.register_function(lookup_procedure, 'lookup_procedure')

    try:
        # Mantém o servidor em execução
        binder_server.serve_forever()
    except KeyboardInterrupt:
        print('bye')