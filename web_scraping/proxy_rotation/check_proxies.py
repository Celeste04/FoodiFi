# tutorial from https://www.youtube.com/watch?v=FbtCl9jJyyc&t=578s
import threading
import queue
import requests

q = queue.Queue()
valid_proxies=[]

with open("proxylist.txt","r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global g
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",proxies={"http":proxy, "https:":proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)

for t in range(10):
        threading.Thread(target=check_proxies())

