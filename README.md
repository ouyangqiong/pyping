pyping
======

A simple pure python ping implementation using unprivileged icmp
socket. Since Linux Kernel 3.0, a new icmp socket was added, check
kernel commit c319b4d76 for the detail.

To use this module, icmp socket privilege should be granted by

```
   sysctl -w net.ipv4.ping_group_range='0  100000'
```
   
