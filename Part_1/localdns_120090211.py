import socket
import dnslib
from dnslib import QTYPE,RR
from dnslib.bimap import Bimap, BimapError
import random

local_server="127.0.0.1"
port=1234
flag=0
cache={}
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((local_server,port))


root_DNS_servers=[
        ["A.root-servers.net",'198.41.0.4'],
        ["B.root-servers.net",'192.228.79.201'],
        ["C.root-servers.net",'192.33.4.12'],
        ["D.root-servers.net",'128.8.10.90'],
        ["E.root-servers.net",'192.203.230.10'],
        ["F.root-servers.net",'192.5.5.241'],
        ["G.root-servers.net",'192.112.36.4'],
        ["H.root-servers.net",'128.63.2.53'],
        ["I.root-servers.net",'192.36.148.17'],
        ["J.root-servers.net",'192.58.128.30'],
        ["K.root-servers.net",'193.0.14.129'],
        ["L.root-servers.net",'198.32.64.12'],
        ["M.root-servers.net",'202.12.27.33'],
    ]


def Publicserver(data):
    global cache
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data,("114.114.114.114",53))
    answer,addr=s.recvfrom(1024)
    d=dnslib.DNSRecord.parse(answer)
    cache[d.q.qname]=str(d.rr[-1].rdata)
    print(cache)
    return answer
def RecursiveBrowser(data,addr):
    count=1
    query=dnslib.DNSRecord.parse(data)
    a=query.reply()
    init_name=query.q.qname
    num=random.randint(-1,12)
    des=root_DNS_servers[num][1]
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5.0)
    while(1):
        try:
            s.sendto(data,(des,53))
            res,address=s.recvfrom(1024)
            break
        except:
                num=random.randint(-1,12)
                des=root_DNS_servers[num][1]
                continue
    re=dnslib.DNSRecord.parse(res)
    print("Server ",count," packet message:\n")
    count+=1
    print(re)
    newdata=data
    while(1):
        flag=True
        while(re.header.a==0):
            try:
                if(len(re.auth)!=0):
                    target=random.randint(-1,len(re.auth))
                    des=re.auth[target].rdata
                elif(len(re.ar)!=0):
                    target=random.randint(-1,len(re.ar))
                    des=re.ar[target].rdata
                s.sendto(newdata,(str(des),53))
                res,address=s.recvfrom(2048)
                re=dnslib.DNSRecord.parse(res)
                print("Server ",count," packet message:\n")
                count+=1
                print(re)
                print("\n")
            except:
                continue
        if(QTYPE[re.a.rtype]=='CNAME'):
            if(flag):
                #a.add_answer(RR(query.q.qname,QTYPE.CNAME,rdata=re.rr[0].rdata))
                flag=False
            try:
                oldname=query.q.qname
                query.q.qname=str(re.rr[0].rdata)
                newdata=query.pack()
                num=random.randint(-1,12)
                s.sendto(newdata,(root_DNS_servers[num][1],53))
                res,address=s.recvfrom(2048)
                a.add_answer(RR(oldname,QTYPE.CNAME,rdata=re.rr[0].rdata))
                re=dnslib.DNSRecord.parse(res)
                print("Server ",count," packet message:\n")
                count+=1
                print(re)
                print("\n")
                flag=True
            except:
                query.q.qname=init_name
                continue
        else:
            a.add_answer(RR(query.q.qname,QTYPE.A,rdata=re.rr[0].rdata))
            cache[init_name]=str(re.rr[0].rdata)
            break
    a.q.qname=init_name
    res=a.pack()
    return res
    
# dig www.baidu.com @127.0.0.1 -p 1234
def main():
    flag=eval(input("please input your choice:\nUse public server-------0\nUse Recursive server-----1: "))
    print(flag)
    while True:
        data,addr=s.recvfrom(2048)
        d=dnslib.DNSRecord.parse(data)
        if d.q.qname in cache:
            res=dnslib.DNSRecord(q=dnslib.DNSQuestion(d.q.qname))
            res.add_answer(dnslib.RR(d.q.qname,dnslib.QTYPE.A, ttl=60,rdata=dnslib.A(cache[d.q.qname])))
            res.header.id=d.header.id
            res=res.pack()
            print("From Cache\n")
            s.sendto(res,addr)
        else:
            if (flag==0):
                res=Publicserver(data)
                s.sendto(res,addr)
                print("From Public Server\n")

            else:
                res=RecursiveBrowser(data,addr)
                s.sendto(res,addr)
                print("From Recursive Server\n")


if __name__ == '__main__':
    main()
