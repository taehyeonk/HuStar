import sys
import heapq

t = int(sys.stdin.readline())
result = []

for _ in range(t):
    hq = []
    for _ in range(int(sys.stdin.readline())):
        query = int(sys.stdin.readline())
        if query != -1:
            heapq.heappush(hq, query)
        else:
            result.append(heapq.heappop(hq))

for i in result:
    print(i)