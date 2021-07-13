import sys

t = int(sys.stdin.readline())

for _ in range(t):
    n, m = map(int, sys.stdin.readline().split())
    plane = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

    dp = [[0]*m for _ in range(n)]

    dp[0][0] = plane[0][0]

    for i in range(1, n):
        dp[i][0] = dp[i-1][0] + plane[i][0]

    for i in range(1, m):
        dp[0][i] = dp[0][i-1] + plane[0][i]

    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = max(dp[i-1][j] + plane[i][j], dp[i][j-1] + plane[i][j])

    print(dp[n-1][m-1])