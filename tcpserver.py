import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

#�B�zclient��thread

def handle_client(client_socket):
    
    #��� cleint �e�Ӫ����
    request = client_socket.recv(1024)
    
    print "[*] Recieved :%s" % request
    
    #�^�Ǥ@�ӫʥ]
    client_socket.send("ACK!")
    
    client_socket.close()
    
while True:
    client, addr = server.accept()
    
    print "[*] Accept connection from: %s:%d" % (addr[0], addr[1])
    
    #�Ұʧڭ̪� client thread �B�z�ǨӪ����
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
    
    