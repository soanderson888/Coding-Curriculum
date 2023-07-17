import time
from scapy.all import *

def traceroute(destination):
    ttl = 1
    while True:
        packet = IP(dst=destination, ttl=ttl) / ICMP()

        start_time = time.time()
        reply = sr1(packet, verbose=0, timeout=1)

        if reply is not None and reply.type == 11:
            rtt = (time.time() - start_time) * 1000
            print(f"{ttl}. {reply.src}  RTT: {rtt:.2f} ms")
        elif reply is not None and reply.type == 0:
            rtt = (time.time() - start_time) * 1000
            print(f"{ttl}. {reply.src}  RTT: {rtt:.2f} ms")
            break

        if reply is not None and reply.dst == destination or ttl >= 64:
            break

        ttl += 1

userinput=input("give a destination IP address")
traceroute(userinput)
