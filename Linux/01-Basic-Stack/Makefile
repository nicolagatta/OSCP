CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie -z execstack

all: vulnerable-x86 vulnerable-x64

vulnerable-x86: vulnerable.c
	$(CC) -o vulnerable-x86 vulnerable.c -m32 $(CFLAGS)

vulnerable-x64: vulnerable.c
	$(CC) -o vulnerable-x64 vulnerable.c $(CFLAGS)

clean: vulnerable-x86 vulnerable-x64 
	rm -f vulnerable-x64 vulnerable-x86
