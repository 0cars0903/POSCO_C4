# test case HeadQ)(Library)
import heapq
for i in range(int(input())):
    A = list(map(int, input().split()))
    HQ = []
    ans = []
    for i in A:
        if i != -1:
            heapq.heappush(HQ, i)
        else:
            ans.append(heapq.heappop(HQ))
    print(*ans)