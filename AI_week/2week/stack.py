# test case
for i in range(int(input())):
    A = list(map(int, input().split()))
    B = []
    for i in A:
        if i != -1:
            B.append(i)
        else:
            print(B.pop(), end = ' ')