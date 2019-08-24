#include <cstdio>

using namespace std;

int main(int argc, char **argv) {
	int ch = 0;
	bool is_first = true;
	while ((ch = getchar()) != EOF) {
		if ((char)ch == '"') {
			is_first ? printf("``") : printf("''");
			is_first = !is_first;
		} else putchar(ch);
	}
	return 0;
}