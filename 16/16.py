
UP, RIGHT, DOWN, LEFT = range(4)
LOCATION, DIRECTION = range(2)
COLUMN, ROW = range(2)
map_direction = {'/': [RIGHT, UP, LEFT, DOWN], '\\': [LEFT, DOWN, RIGHT, UP]}

def move_beam(beam: list[list[int], int]):
  match beam[DIRECTION]:
    case 0: beam[LOCATION][ROW] -= 1
    case 1: beam[LOCATION][COLUMN] += 1
    case 2: beam[LOCATION][ROW] += 1
    case 3: beam[LOCATION][COLUMN] -= 1

def location_inside(position: list[int], width: int, height: int) -> bool:
  return position[ROW] >= 0 and position[ROW] < height and position[COLUMN] >= 0 and position[COLUMN] < width

file_name = 'data.txt'

contraption = [line for line in open(file_name).read().splitlines()]
width = len(contraption[0])
height = len(contraption)

def turn_beam(beam: list[list[int], int], current_field: int, split_beam: bool) -> list[list[int], int]:
  new_beam = None
  _, direction = beam
  if current_field == '.' or (current_field == '|' and direction in [UP, DOWN]) or (current_field == '-' and direction in [LEFT, RIGHT]):
    move_beam(beam)
  elif current_field == '|' and (direction == RIGHT or direction == LEFT):
    beam[DIRECTION] = UP
    if split_beam:
      new_beam = [[i for i in beam[LOCATION]], DOWN]
      move_beam(new_beam)
    move_beam(beam)
  elif current_field == '-' and (direction == UP or direction == DOWN):
    beam[DIRECTION] = LEFT
    if split_beam:
      new_beam = [[i for i in beam[LOCATION]], RIGHT]
      move_beam(new_beam)
    move_beam(beam)
  elif current_field == '/' or current_field == '\\':
    beam[DIRECTION] = map_direction[current_field][beam[DIRECTION]]
    move_beam(beam)
  return new_beam

def perform_energy(start_beam: list[list[int], int]) -> int:
  energized = [[0 for _ in range(width)] for _ in range(height)]

  beams = [start_beam]
  loop_counter = 0
  while loop_counter <= 10:
    energizer_counter = 0
    for beam in beams:
      location, _ = beam[LOCATION], beam[DIRECTION]

      # remove beams out of field
      if not location_inside(location, width, height):
        beams.remove(beam)
        continue

      # energize cell
      if not energized[location[ROW]][location[COLUMN]]:
        energized[location[ROW]][location[COLUMN]] = 1
        energizer_counter += 1
        loop_counter = 0
        split_beam = True
      else:
        split_beam = False

      # turn if necessary, create new beam, IF!!! no beam was created here
      current_field = contraption[location[ROW]][location[COLUMN]]
      new_beam = turn_beam(beam, current_field, split_beam)
      if new_beam: beams.append(new_beam)
    # Loop detection
    if energizer_counter == 0:
      loop_counter += 1

  energized_fields = sum([sum(x) for x in energized])
  return energized_fields

############################
# Taks 1
start_beam = [[0,0], RIGHT] # [[x,y], direction]
energy1 = perform_energy(start_beam)
print('Task 1: %d energized' % energy1) # 46 / 7496

############################
# Taks 2
max_energy = 0
# UP/DOWN
for i in range(width):
  start_beam = [[i, 0], DOWN]
  max_energy = max(max_energy, perform_energy(start_beam))

  start_beam = [[i, height-1], UP]
  max_energy = max(max_energy, perform_energy(start_beam))

  start_beam = [[0, i], RIGHT]
  max_energy = max(max_energy, perform_energy(start_beam))

  start_beam = [[width-1, i], UP]
  max_energy = max(max_energy, perform_energy(start_beam))

print('Task 2: %d max energy' % max_energy) # 51 / 7932