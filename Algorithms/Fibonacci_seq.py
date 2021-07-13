import sys

def fibo(n):
    dp = [0 for _ in range(n+1)]

    for i in range(n+1):
        if i == 0:
            dp[0] = 0
        elif i == 1:
            dp[1] = 1
        elif i == 2:
            dp[2] = 1
        else:
            dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

t = int(sys.stdin.readline())

for _ in range(t):
    n = int(sys.stdin.readline())

    print(fibo(n))