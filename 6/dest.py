import numpy as np
import sys

coords = [list(map(int, line.rstrip().split(", "))) for line in sys.stdin]
xs = np.array([x for (x, y) in coords])
ys = np.array([y for (x, y) in coords])

def closest(x, y):
  ds = np.abs(xs - x) + np.abs(ys - y)
  m = np.argmin(ds)
  if np.sum(ds == ds[m]) == 1:
    return m
  return None

INF = 5*max(max(xs), max(ys))

inf = set()
for i, (x,y) in enumerate(coords):
  if closest(INF, y) == i or \
     closest(-INF, y) == i or \
     closest(x, INF) == i or \
     closest(x, -INF) == i:
    inf.add(i)

area = [0]*len(coords)

for x in range(min(xs), max(xs)+1):
  for y in range(min(ys), max(ys)+1):
    c = closest(x, y)
    if c:
      area[c] += 1

fa = np.array(area)
fa[np.array(list(inf))] = 0
maxa = np.max(fa)
print("maxa={}".format(maxa))

MAXD = 10000
n = 0
for x in range(min(xs), max(xs)+1):
  for y in range(min(ys), max(ys)+1):
    d = np.sum(np.abs(xs - x) + np.abs(ys - y))
    if d < MAXD:
      n += 1
print("|d<{}|={}".format(MAXD, n))
