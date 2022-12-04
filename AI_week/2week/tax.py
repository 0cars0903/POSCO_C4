for t in range(int(input())):
    tax = int(input())

    count = []
    coin = [50000, 10000, 5000, 1000, 500, 100]
    for c in coin:
        count.append(tax // c)
        tax = tax % c
    print(sum(count))