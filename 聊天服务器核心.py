# 文件名：server.py
'''
Linux快速使用说明：
打开终端输入 python3 server.py 即可运行
在终端Crtl+C退出程序
'''
'''
Windows快速使用说明:
点击即可运行
'''
'''
这个程序打开了一个服务端用于连接
它可以执行在线Push，发送历史聊天记录
修改服务端：
    在第33~35行
        你可以把host改成本地可以申请的IP地址
        或者用localhost(127.0.0.1)用于测试
    在第38行
        修改服务器主进程的端口
        这决定了客户端第一个连接的端口
在这个程序中添加了大量的调试语句，可酌情注释或修改
按理来说我应该在线程结束时析构以释放线程，但我不会
'''
import socket
import sys,os,time,random
import threading
import traceback

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# pushsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 获取本地主机名
localhost = socket.gethostname()
host=localhost
# host="localhost"
# host="192.168.4.57"
# host可以使用IP地址
hostip=socket.gethostbyname(host)
port = 9999

# 线程子类
class mythr(threading.Thread):
    def __init__(self,target=None,args=None,cts=None,addr=None):
        threading.Thread.__init__(self)
        self.target=target
        self.args=args
        self.result=None
        self.cts=cts
    def __del__(self):
        cts=self.cts
#         online_list.remove(cts)
#         print("DEL it")
    def run(self):
        self.result=self.target(*self.args)

def futcp(clientsocket,addr):
    # 建立客户端连接
    # accept()为阻塞式，被动接受连接
    # accept()返回参数：[套接字对象],[客户端地址]
    # 返回的[客户端地址]是一个元组
#     print("进入futcp")
    ert=initmsg(clientsocket,addr)
    if(ert):
        return futcpdel(addr)
    global msg
    while True:
        try:
            data=clientsocket.recv(1024)
        except:
            print("与["+str(addr[0])+":"+str(addr[1])+"]接收data数据发生错误 连接终止")
            break
        ti=gttime()
        smsg=ti+hpstr(addr)+":"+data.decode("utf-8")+'\n'
        try:
            msgpush(clientsocket,addr,smsg)
        except:
            print("与"+hpstr(addr)+"下放msg数据错误 连接终止")
            break
        msg=msg+smsg
    clientsocket.close()
    return futcpdel(addr)
def futcpdel(addr):
    online_list.remove(addr)
#     print(online_list)
def initmsg(clientsocket,addr):
    #消息初始化 发送服务器信息以及历史聊天记录
    global msg,host,hostip
    print("连接地址: "+hpstr(addr))
    tag='客户端IP&Port:'+ hpstr(addr)+"\r\n"+ \
         "主机名Hostname:"+str(socket.gethostname())+"\r\n"+\
         "服务端IP&Port:"+str(hostip)+":"+str(port)+"\r\n"+"\n\n"
#     print("向["+str(addr[0])+":"+str(addr[1])+"]发送tag数据")
    try:
        clientsocket.send(tag.encode("utf-8"))
    except:
        print("向["+hpstr(addr)+"]发送tag数据错误，连接终止")
#         os.system("pause")
        return 1
    time.sleep(0)#避免阻塞合并 粘包
#     print("向["+str(addr[0])+":"+str(addr[1])+"]发送msg数据")
    try:
        clientsocket.send(msg.encode("utf-8"))
    except:
        print("向["+hpstr(addr)+"]发送msg数据错误，连接终止")
        return 2
def gttime():
    #获取格式时间 返回一个字符串
    temp=time.localtime()[3:6]
    ti="["+str(temp[0])+":"+str(temp[1])+":"+str(temp[2])+"]"
    return ti
def msgpush(clientsocket,addr,smsg):
    #用于处理用户发来的msg
    print("向["+str(addr[0])+":"+str(addr[1])+"]发送smsg数据")
    # 先送回发送msg的客户端
    clientsocket.send(smsg.encode("utf-8"))
    guangbo(smsg,addr)
def guangbo(msg,addr=None):
    # 用于向在线所有除了addr的客户端Push消息
    pushsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("在线客户端数量：",len(online_list))
    print(online_list)
    for i in online_list:
        if(i!=addr):
            pushsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print("Pushing to "+cpstr(i))
            try:
                pushsocket.connect((i[0],i[2]))
                pushsocket.send(msg.encode("utf-8"))
            except:
                print("连接或发送失败"+cpstr(i))
                print(traceback.format_exc())
#             print(cpstr(i)+" 错误码 "+str(ero))
            pushsocket.close()
def connect_cilent(cts,addrq):
    try:
        port_push=cts.recv(1024).decode("utf-8")
    except:
        print(hpstr(addr)+"连接错误")
        return True
    addr=addrq+tuple(port_push)
    online_list.append(addr)
    return False
def hpstr(addr):
    # 整合addr前两项用于输出
    return "["+str(addr[0])+":"+str(addr[1])+"]"
def cpstr(addr):
    # 整合addr第一项和第三项用于输出
    return "["+str(addr[0])+":"+str(addr[2])+"]"


try:
    serversocket.bind((host,port))
except:
    print("服务被占用")
    print("详细错误信息:\n"+traceback.format_exc())
    os.system("pause")
    exit()
print("服务端 "+str(hostip)+":"+str(port))
# 设置最大连接数，超过后排队
serversocket.listen(5)

msg=gttime()+"以后的聊天记录：\n"
thr_list=[]#线程列表
online_list=[]#在线列表
try:
    while True:
        #服务端循环
        clientsocket,addrq = serversocket.accept()#阻塞等待连接
        #套接字回连
        try:
            port_push=clientsocket.recv(1024).decode("utf-8")
        except:
            print(hpstr(addr)+"连接错误")
            continue
        print("已获取 "+hpstr(addrq)+" Pusher端口 "+port_push)
        try:
            port_push=int(port_push)
        except:
            print(hpstr(addr)+"发来错误Pusher端口，错误信息：\n"+traceback.format_exc())
            continue
        addr=addrq+tuple([int(port_push)])
        online_list.append(addr)
        thr=mythr(target=futcp,cts=clientsocket)
        thr.args=(clientsocket,addr)
        thr.start()
        thr_list.append(thr)
        #超长消息清空
        if len(msg)>1024:
            msg=gttime()+"以后的聊天记录：\n"
finally:
    serversocket.close()
#     pushsocket.close()
'''
On 2023.9.29
这是 __XJN__ 的第一个实用型项目
'''