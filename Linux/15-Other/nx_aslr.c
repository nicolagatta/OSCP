#include <stdio.h>

int vuln()
{
	char input[128];

	puts("I am hungry you have to feed me to win this challenge...");
	puts("Now give me some sweet desert:");
	gets(input);
	return 0;
}	

int main()
{
	vuln();
	return 0;
}	
