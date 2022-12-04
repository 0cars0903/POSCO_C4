# list
for _ in range(int(input())):
    N,M = list(map(int, input().split()))
    A = [[]*N for _ in range(N)]
    for m in range(M):
        u, v= list(map(int, input().split()))
        A[u].append(v)
        A[v].append(u)
    for i in range(N):
        B = A[i]
        B = sorted(B)
        print(*B)