import sys

def getList(N, M):
    l = [[] for _ in range(N)]
    for _ in range(M):
        i, j = map(int, sys.stdin.readline().split())
        l[i].append(j)
        l[j].append(i)
    
    return l

t = int(sys.stdin.readline())

for _ in range(t):
    N, M = map(int, sys.stdin.readline().split())
    result = getList(N, M)
    for r in result:
        r.sort()
        print(*r)