from logging import root
from const import *
import rpyc
import socket
from rpyc.utils.server import ThreadedServer


class DepartamentoRH(rpyc.Service):
    exposed_name = "DepartamentoRH"
    serverNotFound = f"Server não encontrado ou não existente"
    serverNotRegister = f"Servidor nao registrado"
    ListDiretorio = {}
    
    def exposed_get_name(self):
        return self.get_service_name()

    def exposed_register(self, serverName, ipAdress, portNum):
        print(root)
        NameRoot = SERVERDIRETOPRIORAIZ_NAME
        self.ListDir.update({serverName : (ipAdress, portNum)})
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
            firstLayerServer = rpyc.connect(SERVERDIRETOPRIORAIZ,PORTDIRETORIORAIZ)
            return firstLayerServer.root.exposed_lookup(serverName)
            

    def exposed_re_register(self, serverName, ipAdress, portNum):
        print(f"Registrando Server Novamente")
        if serverName in self.ListDiretorio:
            print(f"Achou item que vai ser registrado novamente")
            NameRoot = SERVERDIRETOPRIORAIZ_NAME
            self.ListDiretorio[serverName] = (ipAdress, portNum)
            print(f"Registrando Server")
            print(self.ListDiretorio)
            print(f"{NameRoot}:{self.get_service_name()}:{serverName}")
        else:
            print(f"Item nao registrado")
            return self.serverNotRegister

    def exposed_unregister(self, serverName):
        print(f"Removendo Server")
        if  serverName in self.ListDiretorio:
            print(f"Achamos o server a ser removido")
            ElementoRemovido = self.ListDiretorio[serverName]
            print(f"Guardando o elemento: {ElementoRemovido} para ser usado no return")
            self.ListDiretorio.pop(key=serverName)
            print(f"Removendo elemento do servidor")
            return ElementoRemovido
        else:
            print(f"Nao achamos o server a ser removido")
            return self.serverNotRegister

if __name__ == "__main__":

    print(f"Iniciando servidor de diretórios DepartamentoRH nivel 2 na porta: {PORT_DEPRH}")
    serverDirA = ThreadedServer(DepartamentoRH, port = PORT_DEPRH)
    print(f"Conectando ao Server de diretório raiz")  
    conn_SERVERDIRETOPRIORAIZ = rpyc.connect(SERVERDIRETOPRIORAIZ,PORTDIRETORIORAIZ)
    print(f"Obtendo ipadress do servidor de diretórios DepartamentoRH")  
    ipAdress = socket.gethostbyname(socket.gethostname())
    print(f"Registrando no Server de diretório DepartamentoRH no Server de diretório Raiz") 
    conn_SERVERDIRETOPRIORAIZ.root.exposed_register('DepartamentoRH',ipAdress, PORT_DEPRH)
    serverDirA.start()
