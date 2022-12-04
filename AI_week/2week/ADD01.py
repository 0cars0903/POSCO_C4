# ADD01
left = ['{', '[', '(']
right = ['}', ']', ')']
for i in range(int(input())):
    bracket = input()
    stack = []
    correct = True
    for b in bracket:
        if b in left:
            stack.append(b)
        elif len(stack) == 0:
            correct = False
        elif right.index(b) != left.index(stack.pop()):
            correct = False
    if len(stack) != 0:
        correct = False
    if correct == True:
        print('Yes')
    else:
        print('No')
