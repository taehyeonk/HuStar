import sys
import collections

def getList(N, M):
    l = [[] for _ in range(N)]
    for _ in range(M):
        i, j = map(int, sys.stdin.readline().split())
        l[i].append(j)

    for li in l:
        li.sort()
    return l

def BFS(graph, root):
    visited = []
    queue=collections.deque([])

    queue.append(root)

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])
    
    return visited

t = int(sys.stdin.readline())

for _ in range(t):
    N, M = map(int, sys.stdin.readline().split())
    graph = getList(N, M)
    print(*BFS(graph, 0))