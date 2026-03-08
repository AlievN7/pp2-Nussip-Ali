import shutil
import os

# create file
with open("original.txt", "w") as f:
    f.write("This is the original file.")

# copy file
shutil.copy("original.txt", "backup.txt")
print("File copied to backup.txt")

# check existence
if os.path.exists("backup.txt"):
    print("Backup file exists.")

# delete backup
os.remove("backup.txt")
print("Backup file deleted.")