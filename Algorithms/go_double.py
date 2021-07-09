import sys

t = int(sys.stdin.readline())

for _ in range(t):
    n = int(sys.stdin.readline())
    plate = [0] + list(map(int, sys.stdin.readline().split()))

    dp = [float('-inf') for _ in range(n+1)]
    dp[0] = plate[0]
    dp[1] = plate[1]
    
    for i in range(2, n+1):
        if i % 2 == 0:
            d = int(i/2)
            dp[i] = max( max(dp[i-2] + plate[i], dp[i-1] + plate[i]), dp[d] + plate[i] )
        else:
            dp[i] = max(dp[i-2] + plate[i], dp[i-1] + plate[i])
    
    print(dp[n])