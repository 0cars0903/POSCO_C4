def Bi(x,lst,i,j):
    # 종료 조건 1 리스트 크기
    if i > j:
        return -1
    # 중앙값
    mid = (i+j) // 2
    # 종료 조건 2 원하는 값을 찾음
    if x == lst[mid]:
        return mid
    # 재귀 조건
    if x < lst[mid]:
        return Bi(x,lst,i,mid-1)
    else:
        return Bi(x,lst,mid+1,j)

# Binary Detection
for i in range(int(input())):
    n = list(map(int, input().split()))
    m = list(map(int, input().split()))
    n_len = len(n) - 1 
    ans = []
    for x in m:
        ans.append(Bi(x,n,0,n_len))
    print(*ans)