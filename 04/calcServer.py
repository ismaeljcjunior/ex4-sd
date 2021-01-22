import rpyc
import socket
from const import * 
from rpyc.utils.server import ThreadedServer
 
class CalcServer(rpyc.Service):

  def exposed_soma(self, valor1, valor2):
    
    print(f"Somando valor: {valor1} e {valor2}")
   
    return valor1 + valor2
  def exposed_sub(self, valor1, valor2):
    
    print(f"Subtraindo valor: {valor1} e {valor2}")
   
    return valor1 - valor2

  def exposed_mult(self, valor1, valor2):
    
    print(f"Multiplicando valor: {valor1} e {valor2}")
   
    return valor1 * valor2

  def exposed_div(self, valor1, valor2):
    
    print(f"Dividindo valor: {valor1} e {valor2}")
   
    return valor1 / valor2
           
if __name__ == "__main__":
  print(f"Criando server {SERVER_CALCSERVER_NAME}") 
  server = ThreadedServer(CalcServer, port = PORT_CALCSERVER)
  print(f"Conectando ao Server de diretório DerpartamentoVendas")  
  conn_serverDepVenda = rpyc.connect(SERVER_DEPVENDA,PORT_DEPVENDA)
  print(f"Conectando ao Server de diretório DepartamentoRH")  
  conn_serverDepRh = rpyc.connect(SERVER_DEPRH,PORT_DEPRH)
  print(f"Obtendo ipadress da {SERVER_CALCSERVER_NAME}")  
  ipAdress = socket.gethostbyname(socket.gethostname())
  print(f"Registrando no Server de diretório DerpartamentoVendas") 
  conn_serverDepVenda.root.exposed_register(SERVER_CALCSERVER_NAME,ipAdress,PORT_CALCSERVER)
  print(f"Registrando no Server de diretório DepartamentoRH") 
  conn_serverDepRh.root.exposed_register(SERVER_CALCSERVER_NAME,ipAdress,PORT_CALCSERVER)
  server.start()

