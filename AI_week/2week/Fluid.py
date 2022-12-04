for t in range(int(input())):
    N, C = map(int, input().split())
    bottle = []
    weight = 0
    for n in range(N):
        W, V = (map(int, input().split()))
        bottle.append([W/V, W, V])
    bottle.sort(reverse=True)
    for i in range(N):
        if C >= bottle[i][2]:
            weight = weight + bottle[i][1]
            C = C - bottle[i][2]
        elif C <= bottle[i][2]:
            weight = weight + C*(bottle[i][0])
            break
    print(int(weight))