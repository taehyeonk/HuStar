import sys

def good_mod(n, k, m):
    if k <= 1:
        return (n**k) % m
    else:
        a = k//2
        if k % 2 == 0:
            return ( good_mod(n, a, m)**2 ) % m
        else:
            return ( good_mod(n, a, m)**2 * n ) % m

t = int(sys.stdin.readline())

for _ in range(t):
    n, k, m = map(int, sys.stdin.readline().split())
    print(good_mod(n, k, m))