CC=gcc
CFLAGS=-I. -fno-stack-protector -fno-pie -no-pie 

all: vuln-32 vuln-64

vuln-32: source.c
	$(CC) -o vuln-32 source.c -m32 $(CFLAGS)

vuln-64: source.c
	$(CC) -o vuln-64 source.c $(CFLAGS)

clean: vuln-32 vuln-64 
	rm -f vuln-32 vuln-64
