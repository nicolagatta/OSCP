CC=gcc
CFLAGS=-I. -fno-pie -no-pie -fstack-protector 

all: vuln-32 vuln-64

vuln-32: vulnerable.c
	$(CC) -o vuln-32 vulnerable.c -m32 $(CFLAGS)

vuln-64: vulnerable.c
	$(CC) -o vuln-64 vulnerable.c $(CFLAGS)

clean: vuln-32 vuln-64 
	rm -f vuln-32 vuln-64
