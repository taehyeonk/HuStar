import sys

def getMaxSum(seq):
    # # 브루스포스
    # max_sum = seq[0]

    # for repeat in range(len(seq)):
    #     for i in range(len(seq) - repeat):
    #         subSum = 0
    #         for j in range(repeat+1):
    #             subSum += seq[i+j]
    #         if subSum > max_sum:
    #             max_sum = subSum

    # return max_sum

    # 동적계획법
    dp = [0 for _ in range(len(seq))]
    dp[0] = seq[0]
    max_val = dp[0]

    for i in range(1, len(seq)):
        dp[i] = max(dp[i-1] + seq[i], seq[i])
        max_val = max(max_val, dp[i])
    
    return max_val

t = int(sys.stdin.readline())

for _ in range(t):
    seq = list(map(int, sys.stdin.readline().split()))
    print(getMaxSum(seq))