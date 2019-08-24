#include <cstdio>
#include <cctype>

using namespace std;

char decode(char ch) {
	char table[26] = {'d', 'm', 'b', 'g', 't',
		'h', 'j', 'k', 'p', 'l', ';', '\'',
		'.', ',', '[', ']', 'e', 'y', 'f',
		'u', 'o', 'n', 'r', 'v', 'i', 'c'};
	for (int i = 0; i < 26; i++)
		if (tolower(ch) == table[i]) return (char)('a' + i);
	return ch;
}

int main(int argc, char **argv) {
	int ch = 0;
	while ((ch = getchar()) != EOF) putchar(decode((char)ch));
	return 0;
}