import attr
import numpy as np
import sys
import re

PAT = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')
tuples = []
for line in sys.stdin:
  m = PAT.search(line)
  if not m:
    raise ValueError(line)
  tuples.append(list(map(int, m.groups())))

xs = np.array([t[0] for t in tuples])
ys = np.array([t[1] for t in tuples])

dx = np.array([t[2] for t in tuples])
dy = np.array([t[3] for t in tuples])

def printit(t):
  print("t={}".format(t))
  miny = np.min(ys)
  maxy = np.max(ys)
  minx = np.min(xs)
  maxx = np.max(xs)
  grid = np.zeros(((maxx-minx+1), (maxy-miny+1)))
  for x,y in zip(xs, ys):
    grid[x-minx,y-miny] = 1
  for row in np.transpose(grid):
    for cell in row:
      if cell:
        sys.stdout.write('#')
      else:
        sys.stdout.write('.')
    sys.stdout.write("\n")

t = 0
while True:
  w = np.max(xs) - np.min(xs)
  h = np.max(ys) - np.min(ys)
  if max(w, h) < 200:
    printit(t)
  xs += dx
  ys += dy
  t += 1
