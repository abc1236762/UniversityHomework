// Wrong Answer

#include <cstdio>
#include <vector>

using namespace std;

int main(int argc, char **argv) {
	int ch = 0, idx = 0;
	vector<string> text(1);
	while ((ch = getchar()) != EOF) {
		if ((char)ch == '\n') {
			idx++;
			text.emplace_back("");
			continue;
		}
		if ((char)ch != '\t') text[idx] += (char)ch;
	}
	for (int i = 0; i < 100; i++) {
		bool is_blanked = true;
		for (int j = (int)text.size() - 1; j >= 0; j--) {
			if (text[j].size() > i) {
				putchar(text[j][i]);
				is_blanked = false;
			}
		}
		putchar('\n');
		if (is_blanked) break;
	}
	return 0;
}