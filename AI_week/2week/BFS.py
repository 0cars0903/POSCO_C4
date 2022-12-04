from collections import deque
# list
for _ in range(int(input())):
    N,M = list(map(int, input().split()))
    matrix = [[]*N for _ in range(N)]
    for m in range(M):
        u, v= list(map(int, input().split()))
        matrix[u].append(v)
        
    for i in range(N):
        matrix[i].sort()
    
    visited = [False]*N
    Q = deque([0])
    V = []
    
    while Q:
        v = Q.popleft()
        V.append(v)
        for i in matrix[v]:
            if not (visited[i]):
                Q.append(i)
                visited[i] = True
    print(*V)