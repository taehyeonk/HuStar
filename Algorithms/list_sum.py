import sys

N = int(sys.stdin.readline())
result = []

for i in range(N):
    l = int(sys.stdin.readline().split())
    result.append(sum(l))

for i in result:
    print(i)