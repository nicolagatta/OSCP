CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie 

all: vuln-32 vuln-64

vuln-32: nx_aslr.c
	$(CC) -o vuln-32 nx_aslr.c -m32 $(CFLAGS)

vuln-64: nx_aslr
	$(CC) -o vuln-64 nx_aslr.c $(CFLAGS)

clean: vuln-32 vuln-64 
	rm -f vuln-32 vuln-64
