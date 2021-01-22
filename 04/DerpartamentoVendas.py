from logging import root
from const import *
import rpyc
import socket
from rpyc.utils.server import ThreadedServer


class DerpartamentoVendas(rpyc.Service):
    
    exposed_name = "DerpartamentoVendas"
    serverNotFound = f"Server não encontrado ou não existente"
    serverNotRegister = f"Servidor nao registrado"
    ListDiretorio = {}

    def exposed_get_name(self):
        return self.get_service_name()
    
    def exposed_register(self, serverName, ipAdress, portNum):

        print(root)
        NameRoot = SERVERDIRRAIZ_NAME
        self.ListDir[serverName] = (ipAdress, portNum)
        print(f"Registrando Server")
        print(self.ListDir)
        print(f"{NameRoot}:{self.get_service_name()}:{serverName}")
        
    def exposed_lookup(self, serverName):
        print(f"Buscando Server")

        if  serverName in self.ListDir:
            print(f"Server encontrado")
            return self.ListDir[serverName]
        else:
            print(f"Nao encontrado server local, voltando ao server raiz")
            firstLayerServer = rpyc.connect(SERVERDIRRAIZ,PORTDIRRAIZ)
            return firstLayerServer.root.exposed_lookup(serverName)
        
    def exposed_re_register(self, serverName, ipAdress, portNum):
        print(f"Registrando Server Novamente")
        if serverName in self.ListDir:
            print(f"Achou item que vai ser registrado novamente")
            NameRoot = SERVERDIRRAIZ_NAME
            self.ListDir[serverName] = (ipAdress, portNum)
            print(f"Registrando Server")
            print(self.ListDir)
            print(f"{NameRoot}:{self.get_service_name()}:{serverName}")
        else:
            print(f"Item nao registrado")
            return self.serverNotRegister
        

    def exposed_unregister(self, serverName):
        print(f"Removendo Server")
        if  serverName in self.ListDir:
            print(f"Achamos o server a ser removido")
            ElementoRemovido = self.ListDir[serverName]
            print(f"Guardando o elemento: {ElementoRemovido} para ser usado no return")
            self.ListDir.pop(key=serverName)
            print(f"Removendo elemento do servidor")
            return ElementoRemovido
        else:
            print(f"Nao achamos o server a ser removido")
            return self.serverNotRegister
        

if __name__ == "__main__":
    
    print(f"Iniciando servidor de diretórios DerpartamentoVendas nivel 2 na porta: {PORT_DEPVENDA}")
    serverDirA = ThreadedServer(DerpartamentoVendas, port = PORT_DEPVENDA)
    print(f"Conectando ao Server de diretório raiz")  
    conn_serverDirRaiz = rpyc.connect(SERVERDIRRAIZ,PORTDIRRAIZ)
    print(f"Obtendo ipadress do servidor de diretórios DerpartamentoVendas")  
    ipAdress = socket.gethostbyname(socket.gethostname())
    print(f"Registrando no Server de diretório DerpartamentoVendas no Server de diretório Raiz") 
    conn_serverDirRaiz.root.exposed_register('DerpartamentoVendas',ipAdress,PORT_DEPVENDA)
    serverDirA.start()
