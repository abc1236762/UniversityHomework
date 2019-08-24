#include <stdio.h>

int GCD(long long, long long);

int LCM(long long, long long);

int main() {
    int m = 0;
    while (scanf("%d", &m) != EOF) {
        int n = 0, i = 0, j = 0, N1 = 0, N2 = 0;
        for (i = 0; i < m; i++) {
            scanf("%d", &n);
            scanf("%d", &N1);
            for (j = 0; j < n - 1; j++) {
                scanf("%d", &N2);
                N1 = LCM(N1, N2);
            }
            printf("%d\n", N1);
        }
    }
    return 0;
}

int GCD(long long N1, long long N2) {
    if (N2) while ((N1 %= N2) && (N2 %= N1));
    return N1 + N2;
}

int LCM(long long N1, long long N2) {
    return N1 * N2 / GCD(N1, N2);
}