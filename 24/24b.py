from utils import *

lines = open('aoc/day24.in').read().splitlines()

arr = []
for line in lines:
    left, right = line.split(' @ ')
    px, py, pz = list(map(int, left.split(', ')))
    vx, vy, vz = list(map(int, right.split(', ')))
    arr.append((px, py, pz, vx, vy, vz))

def sol2(x1, y1, z1, v1x, v1y, v1z):
    # (x-x1)/(vx-v1x)=(y-y1)/(vy-v1y)=(z-z1)/(vz-v1z)
    cur = f'(x-{x1})/(a-{v1x})=(y-{y1})/(b-{v1y})=(z-{z1})/(c-{v1z})'
    cur = cur.replace('--','+')
    return cur

for i in range(4):
    cur = sol2(*arr[i])
    print(cur, '\n')

# Solve by 'system of four equations' on WA

x, y, z = 131246724405205, 399310844858926, 277550172142625
print(x+y+z)