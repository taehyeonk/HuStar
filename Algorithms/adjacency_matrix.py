import sys

def getMatrix(N, M):
    l = [[0]*N for _ in range(N)]
    for _ in range(M):
        i, j, k = map(int, sys.stdin.readline().split())
        l[i][j] = k
    
    return l

t = int(sys.stdin.readline())

for _ in range(t):
    N, M = map(int, sys.stdin.readline().split())
    result = getMatrix(N, M)
    for r in result:
        print(*r)