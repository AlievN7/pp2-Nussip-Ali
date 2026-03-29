filename = "database.ini"

with open(filename, "rb") as f:
    data = f.read()

print(data[50:70])  # вывод байтов около позиции 61
print("Байт на позиции 61:", data[61])