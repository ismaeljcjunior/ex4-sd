from logging import root
from threading import local
from const import *
import rpyc
from rpyc.utils.server import ThreadedServer


class ServerDirRaiz(rpyc.Service):
    exposed_name = "ServerDirRaiz"
    serverNotFound = f"Server não encontrado ou não existente"
    serverNotRegister = f"Servidor nao registrado"
    ListDiretorio = {}

    def exposed_get_name(self):
        return self.get_service_name()

    def exposed_register(self, serverName, ipAdress, portNum):
        print(root)
        self.ListDiretorio[serverName] = (ipAdress, portNum)
        print(f"Registrando Server")
        print(self.ListDiretorio)
        print(f"{self.get_service_name()}:{serverName}")

    def exposed_lookup(self, serverName):

        print(f"Buscando Server")
        ListNames = serverName.split(":")
        print(ListNames)

        if len(ListNames) > 0:

            if ListNames[NAMEROOT] in self.ListDiretorio:
                print(f"Verificando se existe segunda camada")

                if len(ListNames) > 1:
                    secondLayerIP = self.ListDiretorio[ListNames[NAMEROOT]][0]
                    secondLayerPort = self.ListDiretorio[ListNames[NAMEROOT]][1]

                    print(f"Existe segunda camada, vamos conectar em ip: {secondLayerIP} e porta: {secondLayerPort}")
                    secondLayerServer = rpyc.connect(secondLayerIP, secondLayerPort)
                    print(f"Buscando Server na segunda camada com nome de: {ListNames[NAMESERVE]}")
                    return secondLayerServer.root.exposed_lookup(ListNames[NAMESERVE])
                else:
                    print(f"Server encontrado")
                    return self.ListDir[ListNames[NAMEROOT]]
            else:
                print(f"Server não encontrado")
                return self.serverNotFound
        else:
            print(f"Server não encontrado")
            return self.serverNotFound

    def exposed_re_register(self, serverName, ipAdress, portNum):

        print(f"Registrando Server Novamente")
        if serverName in self.ListDir:
            print(f"Achou item que vai ser registrado novamente")
            self.ListDir[serverName] = (ipAdress, portNum)
            print(f"Registrando Server")
            print(self.ListDir)
            print(f"{self.get_service_name()}:{serverName}")
        else:
            print(f"Item nao registrado")
            return self.serverNotRegister

    def exposed_unregister(self, serverName):
        print(f"Removendo Server")
        if serverName in self.ListDir:
            print(f"Achamos o server a ser removido")
            ElementoRemovido = self.ListDir[serverName]
            print(
                f"Guardando o elemento: {ElementoRemovido} para ser usado no return")
            self.ListDir.pop(key=serverName)
            print(f"Removendo elemento do servidor")

        else:
            print(f"Nao achamos o server a ser removido")
            return self.serverNotRegister


if __name__ == "__main__":

    print(f"Iniciando servidor de diretórios na porta: {PORTDIRETORIORAIZ}")
    serverDir = ThreadedServer(ServerDirRaiz, port=PORTDIRETORIORAIZ)
    serverDir.start()
