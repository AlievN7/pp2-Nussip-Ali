def sTOn(n):
    x = ""
    x1 = list(n)
    x2 = ""
    for i in range(0, len(x1), 3):
        if x1[i] != "-" and x1[i] != "+" and x1[i] != "*":
            x2 += x1[i] + x1[i + 1] + x1[i + 2]
            if x2 == "ONE":
                x += "1"
            elif x2 == "TWO":
                x += "2"
            elif x2 == "THR":
                x += "3"
            elif x2 == "FOU":
                x += "4"
            elif x2 == "FIV":
                x += "5"
            elif x2 == "SIX":
                x += "6"
            elif x2 == "SEV":
                x += "7"
            elif x2 == "EIG":
                x += "8"
            elif x2 == "NIN":
                x += "9"
    return x

def nTOs(n):
    s = ""
    while n != 0:
        if n == 1:
            s += "ONE"
        elif n == 2:
            s += "TWO"
        elif n == 3:
            s += "THR"
        elif n == 4:
            s += "FOU"
        elif n == 5:
            s += "FIV"
        elif n == 6:
            s += "SIX"
        elif n == 7:
            s += "SEV"
        elif n == 8:
            s += "EIG"
        elif n == 9:
            s += "NIN"
        n //= 10
    return s
q = int(input())
n = input()
print(nTOs(q))
print(sTOn(n))