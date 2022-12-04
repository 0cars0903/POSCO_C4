INF = float('inf')
# 인접 리스트 생성
for _ in range(int(input())):
    N, M = (map(int, input().split()))
    matrix = [[0]*N for _ in range(N)]
    for _ in range(M):
        u, v, c= (map(int, input().split()))
        matrix[u][v] = c

visit = [False]*N
dist = [INF]*(N)
dist[0] = 0
for _ in range(N):
    Min = INF
    for i in range(N):
        if visit[i] == False and dist[i] < Min:
            Min = dist[i]
            id = i
    if Min == INF: break
    visit[id] = True
    for i in range(N):
        if matrix[id][i] != 0 and dist[id] + matrix[id][i] < dist[i]:
            dist[i] = dist[id] + matrix[id][i]
if visit[N-1] == False:
    print(-1)
else:
    print(dist[-1])