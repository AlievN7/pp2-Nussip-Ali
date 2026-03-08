import shutil
import os

# create a file
with open("move_example.txt", "w") as f:
    f.write("File to move")

# create directory
os.makedirs("destination", exist_ok=True)

# move file
shutil.move("move_example.txt", "destination/move_example.txt")

print("File moved to destination folder.")