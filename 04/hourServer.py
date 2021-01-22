from logging import root
import rpyc
import socket
from datetime import datetime, time
from const import * 
from rpyc.utils.server import ThreadedServer
 
class HourServer(rpyc.Service):

  
  def exposed_hourNow(self, nameServer):
    return f"FQN:{nameServer}:{self.get_service_name()} Hour:{datetime.now()}"

   
           
if __name__ == "__main__":

  print(f"Criaando server HourServer") 
  server = ThreadedServer(HourServer, port = PORT_HOURSERVER)
  print(f"Conectando ao Server de diretório DerpartamentoVendas")  
  conn_serverDepVenda = rpyc.connect(SERVER_DEPVENDA,PORT_DEPVENDA)
  print(f"Conectando ao Server de diretório DepartamentoRH")  
  conn_serverDepRH = rpyc.connect(SERVER_DEPRH,PORT_DEPRH)
  print(f"Obtendo ipadress da HourServer")  
  ipAdress = socket.gethostbyname(socket.gethostname())
  print(f"Registrando no Server de diretório DerpartamentoVendas") 
  conn_serverDepVenda.root.exposed_register('HourServer',ipAdress,PORT_HOURSERVER)
  print(f"Registrando no Server de diretório DepartamentoRH") 
  conn_serverDepRH.root.exposed_register('HourServer',ipAdress,PORT_HOURSERVER)

  server.start()


