import sys

T = int(sys.stdin.readline())

for _ in range(T):
    cost = int(sys.stdin.readline())
    count = 0

    if cost // 50000 > 0:
        count += cost//50000
        cost = cost % 50000
    
    if cost // 10000 > 0:
        count += cost//10000
        cost = cost % 10000
    
    if cost // 5000 > 0:
        count += cost//5000
        cost = cost % 5000
    
    if cost // 1000 > 0:
        count += cost//1000
        cost = cost % 1000

    if cost // 500 > 0:
        count += cost//500
        cost = cost % 500
    
    if cost // 100 > 0:
        count += cost//100
        cost = cost % 100
    
    print(count)
