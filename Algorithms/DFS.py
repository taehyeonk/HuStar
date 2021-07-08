import sys

def getList(N, M):
    l = [[] for _ in range(N)]
    for _ in range(M):
        i, j = map(int, sys.stdin.readline().split())
        l[i].append(j)
        l[j].append(i)

    for li in l:
        li.sort(reverse=True)
    return l

def DFS(graph, root):
    visited = []
    stack = []

    stack.append(root)

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            stack.extend(graph[node])
    
    return visited

t = int(sys.stdin.readline())

for _ in range(t):
    N, M = map(int, sys.stdin.readline().split())
    graph = getList(N, M)
    print(*DFS(graph, 0))