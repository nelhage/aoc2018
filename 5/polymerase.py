import sys
import numpy as np

line = sys.stdin.read().rstrip()

def shrink(line):
  BIT = 32

  i = 0
  j = 0

  arr = np.array(list(map(ord, line)), dtype=np.uint8)
  while j < len(arr):
    if i > 0 and arr[i-1] ^ BIT == arr[j]:
      i -= 1
    else:
      arr[i] = arr[j]
      i += 1
    j += 1
  return i

chars = set(line.lower())
mlen = min(
  shrink(line.replace(c, '').replace(c.upper(), ''))
  for c in chars
)

# print(''.join(map(chr, arr[:i])))
print("min={}".format(mlen))
