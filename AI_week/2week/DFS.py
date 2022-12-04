# Input
for t in range(int(input())):
    N, M = list(map(int, input().split()))
    matrix = [[]*N for _ in range(N)]
    for m in range(M):
        u, v= list(map(int, input().split()))
        matrix[u].append(v)
        matrix[v].append(u)
# 인접 리스트 생성
    for i in range(N):
        matrix[i].sort(reverse=True)
# DFS
    visit = [False]*N
    stack = [0]
    V = []
    while stack:
        v = stack.pop()
        if visit[v] == True:
            continue
        visit[v] = True
        V.append(v)
        for j in matrix[v]:
            if visit[j] == False:
                stack.append(j)

    print(*V)

