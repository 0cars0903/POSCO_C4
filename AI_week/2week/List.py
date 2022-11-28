t = int(input())
for i in range(t):
    A = list(map(int, input().split()))
    print(sum(i for i in A))

