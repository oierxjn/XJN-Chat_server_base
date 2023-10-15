# 文件名：client.py
'''
'''
'''
这是一个客户端用于接收对应服务器发来的数据
拥有Pusher和消息循环
支持多开客户端，将会占用不同的Push端口
修改客户端：
    在第30~31行：
        修改这个host，可以是IP或主机名或(localhost)
        程序将会连接这个host
    在第88行：
        你可以修改这个端口号
        程序将会连接这个端口号的服务器
    在第89行：
        程序将会调用函数自己探测一个可用端口
        你也可以直接赋值这个端口，但要注意一个端口只能连接一个套接字
        这意味着固定端口时一个IP只能开启一个客户端
在这个程序中添加了大量的调试语句，可酌情注释或修改
'''
import socket,traceback
import sys,os,threading,random

#____________全局变量声明______________

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 使用本地主机名或IP
localhost=socket.gethostname()
localhostip=socket.gethostbyname(localhost)
host = localhost
#host="192.168.21.4"
hostip=socket.gethostbyname(host)

#_____________类和函数声明_______________
#线程子类
class mythr(threading.Thread):
    def __init__(self,target,args=None):
        threading.Thread.__init__(self)
        self.target=target
        self.args=args
        self.result=None
    def run(self):
        if(self.args!=None):
            self.result=self.target(*self.args)
        else:
            self.result=self.target()
def purcf():
    # 一个阻断式等待连接的Push接收
    global pst
    while True:
        host_push,addr_push=pst.accept()
        print("Pusher连接成功，接收数据中")
#         try:
        msg=host_push.recv(1024)
#         except:
#             print("服务器Pusher连接错误")
        host_push.close()
        print("Pusher:"+msg.decode("utf=8"))
def check_port_in_use(port, host=socket.gethostname()):
    #检测端口是否在使用
    if port<=1024:
        # 系统端口
        return True
    if port>65535:
        return True
    s = None
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host, int(port)))
        return False
    except socket.error:
        s.close()
        return True
    finally:
        s.close()
def findport():
    #用于找一个没有被用过的端口
    port_push=1025
    #默认从1025开始查找
    while(check_port_in_use(port_push)):
        print("端口"+str(port_push)+"被占用")
        port_push+=1
        #当端口占用数在中等规模(1000~6000)时可以考虑使用random
#         port_push=random.randint(1025,65535)
    return port_push
def hpstr(addr):
    # 整合addr前两项用于输出
    return "["+str(addr[0])+":"+str(addr[1])+"]"
def cpstr(addr):
    # 整合addr第一项和第三项用于输出
    return "["+str(addr[0])+":"+str(addr[2])+"]"

# 设置端口号
port = 9999
print("本机IP："+str(localhostip))
# 连接服务，指定主机和端口

#_____________开始服务______________
try:
    print("尝试连接服务器:"+hpstr((hostip,port)))
    s.connect((host, port))
    print("已连接至服务器"+hpstr((hostip,port)))
#connect函数需要传入一个元组
except:
    print("连接错误:")
    print(traceback.format_exc())
    s.close()
    os.system("pause")
    exit()
try:
    port_pst =findport()
    pst.bind((localhost,port_pst))
    print("Pusher端口绑定完毕 为"+str(port_pst))
except:
    print("无可用Pusher端口")
    s.close()
    pst.close()
    os.system("pause")
    exit()
pst.listen(5)
mty=mythr(target=purcf)
mty.start()
# 接收小于 1024 字节的数据
try:
    s.send(str(port_pst).encode("utf-8"))
    print("发送Pusher Port")
    tag = s.recv(1024)
#     print("接收tag数据")
    print (tag.decode('utf-8'))
#     print("接收msg数据")
    msg = s.recv(1024)
    print (msg.decode('utf-8'))
#     myt=mythr(target=rce,args=())
    while True:# 消息循环
        msg=input("输入你要发送的信息\n")
        s.send(msg.encode("utf-8"))
#     print("接收smsg数据")
        msg = s.recv(1024)
        print("消息发送完成：\n"+msg.decode("utf-8"))
finally:
    print("与服务器断开连接")
    s.close()
    pst.close()
'''
On 2023.9.29
这是 __XJN__ 的第一个实用型项目
'''