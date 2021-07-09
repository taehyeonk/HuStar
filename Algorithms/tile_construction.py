import sys

dist = 1000000

total_type = [0 for _ in range(dist + 1)]
single_end = [0 for _ in range(dist + 1)]

total_type[1] = 2
total_type[2] = 7

single_end[1] = 1
single_end[2] = 3

for i in range(3, dist+1):
    total_type[i] = (total_type[i-1]*2 + total_type[i-2] + single_end[i-1]*2) % 1000000000
    # single_end[i] = (total_type[i] - total_type[i-1]*2 - total_type[i-2])/2 + total_type[i-1]
    single_end[i] = int( (total_type[i] - total_type[i-2])/2 ) % 1000000000


T = int(sys.stdin.readline())

for _ in range(T):
    N = int(sys.stdin.readline())
    print(total_type[N])