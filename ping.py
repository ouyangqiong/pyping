# -*- coding: utf-8 -*-
"""
   A simple pure python ping implementation using unprivileged icmp socket
   
   Since Linux kernel 3.0, a new icmp socket was added, for the detail checking
   kernel commit c319b4d76

   This implementation requires privilege granted by group via
   sysctl -w net.ipv4.ping_group_range='0  100000'

"""

import socket, struct, time

ICMP_ECHO_REQUEST = 8
SOCK_NONBLOCK = 004000

def _recv_ping_resp(sock):
    try:
        sock.recvfrom(1024)
        return True
    except socket.error:
        return False


def ping(targets, timeout=500):
    """
    ping
    
    Check IP reachability of targets using ICMP ECHO request.
    
    targets: sigle host or host list
    timeout: time in ms before stop waiting response from target
    """

    targets = targets if isinstance(targets, list) else [targets]
    socks = [socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM | SOCK_NONBLOCK,
                           socket.IPPROTO_ICMP)
             for x in xrange(len(targets))]
    pkt1 = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, 0, 1)
    pkt2 = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, 0, 2)
    ping_socks = zip(targets, socks)
    for target, sock in ping_socks:
        sock.sendto(pkt1, (target, 1))
        sock.sendto(pkt2, (target, 1))

    time.sleep(timeout/1000.0)

    return [(target, _recv_ping_resp(sock)) for target, sock in ping_socks]


if __name__ == "__main__":
    import pprint
    
    pprint.pprint(ping(['192.168.10.{0}'.format(x) for x in xrange(2, 250)],
                       500))
    pprint.pprint(ping('192.168.10.2'))
