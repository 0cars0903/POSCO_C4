# matrix
for _ in range(int(input())):
    N,M = list(map(int, input().split()))
    Matrix = [[0]*N for _ in range(N)]
    for m in range(M):
        i, j, c = list(map(int, input().split()))
        Matrix[i][j] = c
    for i in range(N):
        B = Matrix[i]
        print(*B)