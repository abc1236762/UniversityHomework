#include <iostream>
#include <cstdio>

using namespace std;

enum ntype { zero, nzero, nan, inf };

struct num {
	int num, den;
	ntype type;
};

template<class T> T gcd(T a, T b) {
	if (b) while ((a %= b) && (b %= a));
	return a + b;
}

num divide(const int n1, const int n2) {
	return n1 ? (n2 ? (num){ n1, n2, nzero } : (num){ n1, 1, inf }) : (n2 ? (num){ 0, n2, zero } : (num){ 0, 0, nan });
}

num com_num(const num n1, num n2, const char op) {
	if (n1.type == nan || n2.type == nan) return { 0, 0, nan };
	switch (op) {
		case '-': // n1 - n2 = n1 + -n2
			n2.num = -n2.num;
		case '+':
			if (n1.type == inf && n2.type == inf) return { n1.num + n2.num, 1, inf };
			if (n1.type == inf) return { n1.num, 1, inf };
			else if (n2.type == inf) return { n2.num, 1, inf };
			return { n1.num * n2.den + n2.num * n1.den, n1.den * n2.den, nzero };
		case '*':
			if ((n1.type == zero && n2.type == inf) || (n1.type == inf && n2.type == zero)) return { 0, 0, nan };
			if (n1.type == inf || n2.type == inf) return { n1.num * n2.num, n1.den * n2.den, inf };
			return { n1.num * n2.num, n1.den * n2.den, nzero };
		default:
			if ((n1.type == inf && n2.type == zero) || (n1.type == zero && n2.type == inf)) return n1;
			if (n1.type == zero && n2.type == zero) return { 0, 0, nan };
			if (n1.type == inf || n2.type == inf) return { n1.num * n2.den, n1.den * n2.num, inf };
			return { n1.num * n2.den, n1.den * n2.num, nzero };
	}
}

void print_num(num n) {
	if (n.type == nzero) n = divide(n.num, n.den);
	if (n.type == zero) printf("0/1\n");
	else if (n.type == nan) printf("NaN\n");
	else if (n.type == inf)
		((n.num < 0 && n.den >= 0) || (n.num >= 0 && n.den < 0)) ? printf("-Infinity\n") : printf("Infinity\n");
	else if (n.type == nzero) {
		int n_gcd = gcd(n.num, n.den);
		if (n.den < 0 && n_gcd > 0) n_gcd = -n_gcd;
		printf("%d/%d\n", n.num / n_gcd, n.den / n_gcd);
	}
}

int main(int argc, char *argv[]) {
	int n = 0;
	while (cin >> n) {
		while (n--) {
			int left = 0, right = 0;
			char op = '\0';
			scanf(" %d/%d", &left, &right);
			num n1 = divide(left, right);
			scanf(" %c", &op);
			scanf(" %d/%d", &left, &right);
			num n2 = divide(left, right);
			print_num(com_num(n1, n2, op));
		}
	}
	return 0;
}
