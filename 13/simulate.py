import attr
import sys
import numpy as np

@attr.s(slots=True)
class Cart:
  x = attr.ib()
  y = attr.ib()
  dir = attr.ib()
  isection = attr.ib(default=0)

text = [list(line.rstrip()) for line in sys.stdin]

rows = len(text)
cols = max(len(row) for row in text)

grid    = np.zeros((cols, rows), dtype=np.uint8)
cartmap = np.zeros((cols, rows), dtype=np.uint8)
carts   = []

for x in range(cols):
  for y in range(rows):
    if x >= len(text[y]):
      cell = ' '
    else:
      cell = text[y][x]
    if cell == '<' or cell == '>':
      cell = '-'
      carts.append(Cart(x, y, cell))
    elif cell == '^' or cell == 'v':
      cell = '|'
      carts.append(Cart(x, y, cell))
    grid[x,y] = ord(cell)
for cart in carts:
  cartmap[cart.x, cart.y] = 1

print("\n".join(''.join(map(chr, row)) for row in np.transpose(grid)))
