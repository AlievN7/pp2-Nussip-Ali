names = ["Ali", "John", "Sara"]
scores = [90, 85, 88]

# enumerate example
print("Using enumerate():")
for index, name in enumerate(names):
    print(index, name)

# zip example
print("\nUsing zip():")
for name, score in zip(names, scores):
    print(name, score)

# sorted example
numbers = [5, 2, 9, 1]
print("\nSorted numbers:", sorted(numbers))