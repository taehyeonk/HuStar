import sys
import collections

t = int(sys.stdin.readline())
result = []

for _ in range(t):
    queue=collections.deque([])
    for _ in range(int(sys.stdin.readline())):
        query = int(sys.stdin.readline())
        if query != -1:
            queue.append(query)
        else:
            result.append(queue.popleft())

for i in result:
    print(i)