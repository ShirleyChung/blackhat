import sys
import socket
import getopt
import threading
import subprocess

#定義一些全域變數
listen  = False
command = False
execute = ""
target  = ""
upload_destination = ""
port = 0

def usage():
    print "BHP Net Tool"
    print
    print "用法: bhpnet.py -t target_host -p port"
    print "-l --listen                    - 在 [host]:[port] 監聽連入連線"
    print "-e --execute=file_to_run       - 接到連線時執行指定檔案"
    print "-c --command                   - 啟動命令列 shell"
    print "-u --upload=destination        - 接到連線時上傳檔案並寫出[destination]"
    print
    print
    print "範例:"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def client_sender(buffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #連到目標主機
        client.connect((target, port))
        
        if (len(buffer)):
            client.send(buffer)
            
        while True:
            #然後等資料回傳
            recv_len = 1
            response = ""
            
            while recv_len:
                data    = client.recv(4096)
                recv_len= len(data)
                response+= data
                
                if recv_len < 4096:
                    break
                
                print response, 
                
                #等待更多輸入
                buffer = raw_input("")
                buffer += "\n"
                
                #傳出去
                client.send(buffer)
    except:
        print "[*] Exception! Exiting."
        
        #拆掉連線
        client.close()
        
def client_handler(client_socket):
    global upload_destination
    global execute
    global command
    
    #檢查上傳
    if len(upload_destination):
        #讀入所有bytes並寫到指定位置
        file_buffer =""
        
        #一直讀到沒有資料為止
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
                
        #然後試著把這些資料存到檔案
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            #回應我們確實把資料存成檔案了
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
            
    if len(execute):
        #執行指令
        output = run_command(execute)
        client_socket.send(output)
        
    if command:
        while True:
            #顯示一個簡單的提示
            client_socket.send("<BHP:#> ")
            #接著持續接收資料, 直到收到LF(Enter鍵)
            cmd_buffer = ""
            
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                
            response = run_command(cmd_buffer)
            
            #回傳
            client_socket.send(response)
            
            
        
def server_loop():
    global target
    
    #若沒定義目標, 就監聽所有介面
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target.port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        #啟動一個thread處理新用戶端
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()
        
def run_command(command):
    #裁掉換行符號
    command = command.rstrip()
    
    #執行指令並取回輸出
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "指令執行失敗\r\n"
    #把輸出傳回用戶端
    return output

    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--listen"):
            execute = a
        elif o in ("-c", "--listen"):
            command = True
        elif o in ("-u", "--listen"):
            upload_destination = a
        elif o in ("-t", "--listen"):
            target = True
        elif o in ("-p", "--listen"):
            port = int(a)
        else:
            assert False, "選項未處理"
            
    #我們要監聽, 還是只是從stdin傳送資料?
    if not listen and len(target) and port > 0:
        #從命令列讀入buffer
        #這會block,所以如果沒有要透過stdin傳資料的話
        #要按CTRL-D
        buffer = sys.stdin.read()
        
        #把資料送出去
        client_sender(buffer)
        
    #我們要監聽, 同時可能根據上面的命令列選項上傳東西,執行指令, 或提供shell
    if listen:
        server_loop()
        
main()
    
    
    
