#include <iostream>
#include <sstream>
#include <stack>

using namespace std;

int main(int argc, char **argv) {
	int n = 0;
	cin >> n, getchar();
	while (n--) {
		string line, tkn;
		getline(cin, line);
		istringstream iss(line);
		stack<int> s;
		while (iss >> tkn) {
			int a = 0, b = 0;
			if (tkn == "+" || tkn == "-" || tkn == "*") {
				b = s.top(), s.pop();
				a = s.top(), s.pop();
				if (tkn == "+") s.push(a + b);
				else if (tkn == "-") s.push(a - b);
				else if (tkn == "*") s.push(a * b);
			} else s.push(atoi(tkn.c_str()));
		}
		cout << s.top() << endl;
	}
}
