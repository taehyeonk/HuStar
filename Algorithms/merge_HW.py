import sys

# <주의> [1:] 과 같은 리스트 슬라이싱을 하면 O(n)만큼 또 시간이 걸리게 된다..
def merge(left, right):
    result = []
    l_idx = 0
    r_idx = 0
    l_max = len(left)
    r_max = len(right)
    while l_idx < l_max or r_idx < r_max:
        if l_idx < l_max and r_idx < r_max:
            if left[l_idx] <= right[r_idx]:
                result.append(1)
                l_idx += 1
            else:
                result.append(2)
                r_idx += 1
        elif l_idx < l_max:
            result.append(1)
            l_idx += 1
        elif r_idx < r_max:
            result.append(2)
            r_idx += 1
    return result

t = int(sys.stdin.readline())

for _ in range(t):
    n = list(map(int, sys.stdin.readline().split()))
    m = list(map(int, sys.stdin.readline().split()))

    print(*merge(n, m))