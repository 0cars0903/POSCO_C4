for t in range(int(input())):
    N = int(input())
    fib = [0] * (N+1)
    for i in range(1, N+1):
        if i == 1:
            fib[i] = 1
        elif i == 2:
            fib[i] = 1
        else:
            fib[i] = fib[i-1] + fib[i-2]
    print(fib[N])
