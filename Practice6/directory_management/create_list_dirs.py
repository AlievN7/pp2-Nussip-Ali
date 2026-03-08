import os

# create directory
os.mkdir("test_dir")

# create nested directories
os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Directories created.")

# show current directory
print("Current directory:")
print(os.getcwd())

# list files and folders
print("\nDirectory contents:")
print(os.listdir())