import attr
import sys
import time
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
      carts.append(Cart(x, y, cell))
      cell = '-'
    elif cell == '^' or cell == 'v':
      carts.append(Cart(x, y, cell))
      cell = '|'
    grid[x,y] = ord(cell)
for cart in carts:
  cartmap[cart.x, cart.y] = 1

# print("\n".join(''.join(map(chr, row)) for row in np.transpose(grid)))

MOVES = {
  '<': (-1, 0),
  '>': ( 1, 0),
  '^': ( 0, -1),
  'v': ( 0, 1),
}
# (left, straight, right)
TURNS = {
  '<': 'v<^',
  '>': '^>v',
  '^': '<^>',
  'v': '>v<',
}
CORNERS = {
  ('>', ord('\\')): 'v',
  ('>', ord('/')):  '^',
  ('<', ord('/')):  'v',
  ('<', ord('\\')): '^',

  ('v', ord('\\')): '>',
  ('v', ord('/')):  '<',
  ('^', ord('/')):  '>',
  ('^', ord('\\')): '<',
}

PRINT = False

tick = 0
remove = set()
while True:
  if PRINT:
    # print("before tick={}".format(tick))
    render = np.copy(grid)
    for cart in carts:
      render[cart.x, cart.y] = ord(cart.dir)
    txt = "\n".join(''.join(map(chr, row)) for row in np.transpose(render))
    sys.stdout.write("\x1b[H\x1b[J")
    print(txt)
    # time.sleep(0.5)

  tick += 1
  carts.sort(key=lambda c: (c.y, c.x))

  tmp = np.zeros(grid.shape, dtype=np.uint8)
  for cart in carts:
    tmp[cart.x, cart.y] = 1
  if not np.all(tmp == cartmap):
    ix, iy = np.unravel_index(np.argmax(tmp != cartmap, axis=None), tmp.shape)
    print("invariant violated at={},{}".format(ix, iy))
    sys.exit(1)

  for cart in carts:
    if id(cart) in remove:
      continue
    cartmap[cart.x, cart.y] = 0
    v = MOVES[cart.dir]
    cart.x += v[0]
    cart.y += v[1]
    if cartmap[cart.x, cart.y]:
      remove.update(id(o) for o in carts if o.x == cart.x and o.y == cart.y)
      if len(remove) != 2:
        print("??? remove={}".format(len(remove)))
        print("carts={}".format([o for o in carts if o.x == cart.x and o.y == cart.y]))
      cartmap[cart.x, cart.y] = 0
      continue
    sq = grid[cart.x, cart.y]
    if sq == ord('+'):
      cart.dir = TURNS[cart.dir][cart.isection % 3]
      cart.isection += 1
    else:
      cart.dir = CORNERS.get((cart.dir, sq), cart.dir)
    cartmap[cart.x, cart.y] = 1

  if remove:
    carts = [c for c in carts if id(c) not in remove]
    remove.clear()
    if len(carts) == 1:
      c = carts[0]
      print("done tick={} pos={},{}".format(tick, c.x, c.y))
      break
    elif len(carts) == 0:
      print("oops, no carts left tick={}".format(tick))
      break
