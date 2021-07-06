import sys
import collections

result = []

def getYesOrNo(rank):
    queue = collections.deque([])
    for i in range(len(rank)):
        if len(queue) == 0:
            queue.append(rank[i])
        else:
            if rank[i] != queue[0]:
                queue.append(rank[i])
            elif rank[i] == queue[0]:
                queue.popleft()
        
    if len(queue) == 0: # 순서가 안 바뀜
        return "NO"
    else:               # 순서가 바뀜
        return "YES"

N = int(sys.stdin.readline())

for _ in range(N):
    rank = list(map(int, sys.stdin.readline().split()))
    result.append(getYesOrNo(rank))

for i in result:
    print(i)