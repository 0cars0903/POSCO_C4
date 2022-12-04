for _ in range(int(input())):
    n, m = map(int, input().split())
    data = []
    for i in range(n):
        data.append(list(map(int, input().split())))
    T = [[0] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                T[i][j] = data[i][j]
            elif i == 0:
                T[i][j] = data[i][j] + T[i][j-1]
            elif j == 0:
                T[i][j] = data[i][j] + T[i-1][j]
            else:
                T[i][j] = min(T[i-1][j], T[i][j-1], T[i-1][j-1]) + data[i][j]

    print(T[n-1][m-1])