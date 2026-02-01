n = int(input())
m = {}
out = []
for i in range(n):
    a = input().split()
    if a[0] == "set":
        m[a[1]] = a[2]
    else:
        if a[1] in m.keys():
            out.append(m[a[1]])
        else:
            out.append("KE: no key " + a[1] + " found in the document")

for _ in out:
    print(_)