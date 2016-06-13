import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

#處理client的thread

def handle_client(client_socket):
    
    #顯示 cleint 送來的資料
    request = client_socket.recv(1024)
    
    print "[*] Recieved :%s" % request
    
    #回傳一個封包
    client_socket.send("ACK!")
    
    client_socket.close()
    
while True:
    client, addr = server.accept()
    
    print "[*] Accept connection from: %s:%d" % (addr[0], addr[1])
    
    #啟動我們的 client thread 處理傳來的資料
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
    
    