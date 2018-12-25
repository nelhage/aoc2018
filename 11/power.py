import numpy as np
import scipy.signal
import sys

grid = np.zeros((300, 300))

# SERIAL = 4842
SERIAL = int(sys.argv[1])

for x in range(300):
  for y in range(300):
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack = x + 1 + 10
    # Begin with a power level of the rack ID times the Y coordinate.
    pw = rack * (y + 1)
    # Increase the power level by the value of the grid serial number (your puzzle input).
    pw += SERIAL
    # Set the power level to itself multiplied by the rack ID.
    pw *= rack
    # Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    pw = (pw % 1000) // 100
    pw -= 5
    grid[x,y] = pw


best = (0,0,0)
max  = -1e6

for sz in range(1, 300):
  conv = scipy.signal.convolve2d(grid, np.ones((sz, sz)), mode='valid')
  x, y = np.unravel_index(np.argmax(conv, axis=None), conv.shape)
  if conv[x,y] > max:
    max = conv[x,y]
    best = (sz, x + 1, y + 1)
  print("size={} x={} y={} max={}".format(sz, x + 1, y + 1, conv[x,y]))

print(best)
