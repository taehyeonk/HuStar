import sys
import bisect

def find(l, x):
    i = bisect.bisect_left(l, x)
    if i == 0:
        return l[0]
    elif i == len(l):
        return l[i-1]
    else:
        if l[i] == x:
            return l[i]
        elif x - l[i-1] <= l[i] - x:
            return l[i-1]
        elif x - l[i-1] > l[i] - x:
            return l[i]

N = int(sys.stdin.readline())

for _ in range(N):
    l = list(map(int, sys.stdin.readline().split()))
    num_list = list(map(int, sys.stdin.readline().split()))
    result = [find(l, num) for num in num_list]
    
    print(*result)