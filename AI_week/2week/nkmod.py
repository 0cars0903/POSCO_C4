def mod(n,m,k):
    # k가 0 일때
    if k == 0:
        return 1
    # k가 짝 수 일때
    if k % 2 == 0:
        mod_value = (mod(n,m,k/2)) % m
        return (mod_value * mod_value) % m
    # k가 홀 수 일 때
    else: 
        mod_value = (mod(n,m,(k-1)/2)) % m
        return (mod_value * mod_value * (n % m)) % m

# mod m 
for i in range(int(input())):
    n, k, m = list(map(int, input().split()))
    ans = []
    ans.append(mod(n,m,k))
    print(*ans)