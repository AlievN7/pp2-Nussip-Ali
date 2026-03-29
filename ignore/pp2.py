l1 = [5, 6, 4]
l2 = [2, 4, 3]
k1 = 0
k2 = 0
for i in range(len(l1)):
    k1 += l1[i] * 10**i

for i in range(len(l2)):
    k2 += l2[i] * 10**i

k12 = k1 + k2
q = list(map(int, str(k12)))
print(q)