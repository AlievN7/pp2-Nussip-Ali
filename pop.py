import re

txt = input()
pattern = input()
x = re.split(pattern, txt)
if x:
  print(*x, sep = ",")