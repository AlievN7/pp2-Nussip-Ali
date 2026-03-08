# write to file (overwrite)
with open("data.txt", "w") as f:
    f.write("First line\n")
    f.write("Second line\n")

print("File written successfully.")

# append new content
with open("data.txt", "a") as f:
    f.write("Appended line\n")

print("Content appended.")

# read to verify
with open("data.txt", "r") as f:
    print("\nFile content:")
    print(f.read())