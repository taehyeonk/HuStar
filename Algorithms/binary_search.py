import sys

def binary_search(l, num):
    left = 0
    right = len(l)-1
    while left <= right:
        mid = (left + right) // 2
        if l[mid] == num:
            break
        elif l[mid] > num:
            right = mid - 1
        elif l[mid] < num:
            left = mid + 1
    if left > right:
        return -1
    else:
        return mid

N = int(sys.stdin.readline())

for _ in range(N):
    l = list(map(int, sys.stdin.readline().split()))
    num_list = list(map(int, sys.stdin.readline().split()))
    result = []

    for num in num_list:
        result.append(binary_search(l, num))
    
    print(*result)