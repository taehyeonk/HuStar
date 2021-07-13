import sys

T = int(sys.stdin.readline())

for _ in range(T):
    N, C = map(int, sys.stdin.readline().split())
    total_weight = 0

    wei_vol = []
    for _ in range(N):
        W, V = map(int, sys.stdin.readline().split())
        wei_vol.append([W/V, W, V])
    
    wei_vol.sort(reverse=True)

    for i in range(N):
        if C != 0:
            if wei_vol[i][2] < C:
                total_weight += wei_vol[i][1]
                C -= wei_vol[i][2]
            else:
                total_weight += int(wei_vol[i][0] * C)
                C -= C
        else:
            break
    
    print(total_weight)

