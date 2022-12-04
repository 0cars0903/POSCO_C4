# test case
import collections 
for i in range(int(input())):
    A = list(map(int, input().split()))
    Q = collections.deque([])
    for i in A:
        if i != -1:
            Q.append(i)
        else:
            print(Q.popleft(), end=" ")


# test case
for i in range(int(input())):
    A = list(map(int, input().split()))
    i = 0
    Q = []
    for i in A:
        if i != -1:
            Q.append(i)
        else:
            print(Q.append(Q[i]), end = ' ')
            i += 1