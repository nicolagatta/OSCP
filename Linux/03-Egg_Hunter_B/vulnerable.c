#include <stdio.h>
#include <stdlib.h>

/************************************************************************
 * The buffer in the heap is long enough for a shellcode
 * The buffer on the stack is short
 * We nedd to use an EGG Hunter
 ************************************************************************/

char BufferOne[500];

void exec_shell() {

        int arg;
        arg = "/bin/sh";
        system(arg);
}

void vuln() {

	char BufferTwo[40];
	printf("Insert Element One:\n");
	fgets(BufferOne,500,stdin);
	
	printf("Insert Element Two:\n");
	fgets(BufferTwo,60,stdin);

}

int main(void) {

	vuln();

}
