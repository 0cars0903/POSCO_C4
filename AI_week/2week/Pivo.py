import sys
sys.setrecursionlimit(1000000)

def pi(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return pi(n-1) + pi(n-2)
    
for i in range(int(input())):
    t = int(input())
    print(pi(t))