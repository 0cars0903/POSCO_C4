for _ in range(int(input())):
    N = int(input())
    cross = [0] * (N+1)
    for i in range(1, N+1):
        if i == 0:
            cross[i] = 0
        elif i == 1:
            cross[i] = 1
        elif i == 2:
            cross[i] = 2
        elif i == 3:
            cross[i] = 4
        else:
            cross[i] = cross[i-1] + cross[i-2] + cross[i-3]
            cross[i] = cross[i] % 1904101441
    print(cross[N])