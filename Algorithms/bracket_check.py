import sys

result = []
close_b = [")", "}", "]"]

def match(bracket):
    if bracket == "(":
        return ")"
    elif bracket == "{":
        return "}"
    elif bracket == "[":
        return "]"

def getYesOrNo(l):
    b_stack = []
    for i in range(len(l)):
        if len(b_stack) == 0:
            if l[i] not in close_b:
                b_stack.append(l[i])
            else:
                return "NO"
        else:
            if l[i] != match(b_stack[-1]) and l[i] in close_b:
                return "NO"
            elif l[i] == match(b_stack[-1]):
                b_stack.pop()
            elif l[i] not in close_b:
                b_stack.append(l[i])
        
    if len(b_stack) == 0:
        return "YES"
    else:
        return "NO"

t = int(sys.stdin.readline())

for _ in range(t):
    b_stack = []
    l = list(sys.stdin.readline().strip())
    result.append(getYesOrNo(l))

for i in result:
    print(i)