#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void vuln() {
    char buf[100];
    gets(buf);
    printf("Your input was %s\n",buf);
    return 0;
}

int main(void) {
    int a;
    printf("Don't forget to disable ASRL with 'echo 0 > /proc/sys/kernel/randomize_va_space' as root user\n");
    printf("Once finished, re-eanble ASRL with 'echo 2 > /proc/sys/kernel/randomize_va_space' as rooot user\n");
    printf("Current stack is at %x\n",&a);
    printf("Enter some input: ");
    vuln();
    return 0;
}
