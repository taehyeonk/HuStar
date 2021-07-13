import sys

t = int(sys.stdin.readline())
result = []

for _ in range(t):
    stack = []
    for _ in range(int(sys.stdin.readline())):
        query = int(sys.stdin.readline())
        if query != -1:
            stack.append(query)
        else:
            result.append(stack.pop())

for i in result:
    print(i)