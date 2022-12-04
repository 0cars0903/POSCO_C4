# Hanoi
def Hanoi(start, mid, end, n):
    if n == 0:
        return
    Hanoi(start, end, mid, n-1)
    print("{0} -> {1}".format(start, end))
    Hanoi(mid, start, end, n-1)

start = 'A'
mid = 'B'
end = 'C'

for i in range(int(input())):
    t = int(input())
    Hanoi(start, mid, end, t)