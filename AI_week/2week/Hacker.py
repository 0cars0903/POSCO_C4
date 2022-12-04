# list
for _ in range(int(input())):
    N,M = list(map(int, input().split()))
    matrix = [[]*N for _ in range(N)]
    for m in range(M):
        u, v= list(map(int, input().split()))
        matrix[u].append(v)
        matrix[v].append(u)
# BFS
    C = []
    c = 0
    visited = [False]*N
    for i in range(N):
        
        if visited[i] == False:
            visited[i] = True
            Q = [i]
            while Q:
                v = Q.pop()
                for j in matrix[v]:
                    if visited[j] == False:
                        Q.append(j)
                        visited[j] = True
            c = c + 1
            C.append(c)
    print(C[-1])