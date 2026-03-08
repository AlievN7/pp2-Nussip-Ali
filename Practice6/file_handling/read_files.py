# create a sample file first
with open("example.txt", "w") as f:
    f.write("Hello Python\n")
    f.write("File handling practice\n")
    f.write("Reading files example")

# read entire file
with open("example.txt", "r") as f:
    print("Using read():")
    print(f.read())

# read line by line
with open("example.txt", "r") as f:
    print("\nUsing readline():")
    print(f.readline())
    print(f.readline())

# read lines into list
with open("example.txt", "r") as f:
    print("\nUsing readlines():")
    lines = f.readlines()
    print(lines)