#ADD02
import collections 
from collections import deque
for i in range(int(input())):
    car = list(map(int, input().split()))
    Q = collections.deque([])
    for c in car:
        if (len(Q) == 0) or (Q[0] != c):
            Q.append(c)
        else:
            Q.popleft()
    if len(Q) != 0:
        print('Yes')
    else:
        print('No')