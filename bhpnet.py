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
    
    
    