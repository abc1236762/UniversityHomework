#include <stdio.h>

typedef struct {
	int val[2][2];
} matrix;

matrix matrix_mul_mod(matrix *mtx1, matrix *mtx2, int mod) {
	return (matrix){{{(mtx1->val[0][0] * mtx2->val[0][0] + mtx1->val[0][1] * mtx2->val[1][0]) % mod,
		(mtx1->val[0][0] * mtx2->val[0][1] + mtx1->val[0][1] * mtx2->val[1][1]) % mod}, {
		(mtx1->val[1][0] * mtx2->val[0][0] + mtx1->val[1][1] * mtx2->val[1][0]) % mod,
		(mtx1->val[1][0] * mtx2->val[0][1] + mtx1->val[1][1] * mtx2->val[1][1]) % mod}}};
}

matrix matrix_pow_mod(matrix *mtx, int n, int mod) {
	if (n <= 1) return *mtx;
	matrix mul_mtx = matrix_mul_mod(mtx, mtx, mod), pow_mtx = matrix_pow_mod(&mul_mtx, n / 2, mod);
	return n % 2 ? matrix_mul_mod(mtx, &pow_mtx, mod) : pow_mtx;
}

int fib_mod(int n, int mod) {
	return matrix_pow_mod(&(matrix){{{1, 1}, {1, 0}}}, n, mod).val[0][0];
}

int main(int argc, char *argv[]) {
	int n = 0, mod = 0;
	while (scanf("%d%d", &n, &mod) != EOF) printf("%d\n", fib_mod(n, mod));
	return 0;
}