import sys


def hanoi(n, A, B, C):
    if n == 0:
        return
    else:
        hanoi(n-1, A, C, B)
        print(A, "->", C)
        hanoi(n-1, B, A, C)

T = int(sys.stdin.readline())
for _ in range(T):
    n = int(sys.stdin.readline())
    hanoi(n, 'A', 'B', 'C')