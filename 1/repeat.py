import sys
import os

seen = set()

fs = [int(l.rstrip("\n")) for l in sys.stdin.readlines()]

cur = 0
while True:
  for d in fs:
    if cur in seen:
      print("dup={}".format(cur))
      sys.exit(0)
    seen.add(cur)
    cur += d
