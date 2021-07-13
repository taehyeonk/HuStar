import sys

t = int(sys.stdin.readline())

for _ in range(t):
    n = int(sys.stdin.readline())

    dp = [0 for _ in range(n+1)]

    if n >= 4:
        dp[0] = 0
        dp[1] = 1
        dp[2] = 2
        dp[3] = 4

        for i in range(4, n+1):
            dp[i] = (dp[i-1] + dp[i-2] + dp[i-3]) % 1904101441

        print(dp[n])
    elif n == 3:
        print(4)
    elif n == 2:
        print(2)
    elif n == 1:
        print(1)
    else:
        print(0)