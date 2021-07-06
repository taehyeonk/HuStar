import sys

N = int(sys.stdin.readline())
result = []

for i in range(N):
    l = list(map(int, sys.stdin.readline().split()))
    result.append(max(l) - min(l))

for i in result:
    print(i)