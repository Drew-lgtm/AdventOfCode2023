using DataStructures

const DIRS = (CartesianIndex(0, -1), CartesianIndex(1, 0),
  CartesianIndex(0, 1), CartesianIndex(-1, 0))
const UP = 1; const RIGHT = 2; const DOWN = 3; const LEFT = 4
const OPPOSITE = (DOWN, LEFT, UP, RIGHT)
const MAX_COST = typemax(Int)

function dijkstra(data::Matrix{Int}, min_dist::Int, max_dist::Int)
  dist = fill(MAX_COST, length(DIRS), max_dist, size(data)...)
  queue = PriorityQueue{CartesianIndex{4}, Int}()
  for p in CartesianIndices(data), dir in eachindex(DIRS), seq in 1:max_dist
    queue[CartesianIndex(dir, seq, p)] = MAX_COST
  end
  for (source, source_dist) in (
    (CartesianIndex(DOWN, 1, 1, 2), data[1, 2]),
    (CartesianIndex(RIGHT, 1, 2, 1), data[2, 1]))
    dist[source] = queue[source] = source_dist
  end
  while !isempty(queue)
    u = dequeue!(queue)
    dist_u = dist[u]
    dist_u == MAX_COST && continue
    for dir in eachindex(DIRS)
      dir == OPPOSITE[u[1]] && continue
      dir == u[1] && u[2] == max_dist && continue
      dir != u[1] && u[2] < min_dist && continue
      xy = CartesianIndex(u[3], u[4]) + DIRS[dir]
      !checkbounds(Bool, data, xy) && continue
      v = CartesianIndex(dir, dir == u[1] ? u[2] + 1 : 1, xy)
      dist_v = get(queue, v, -1)
      dist_v == -1 && continue
      alt = dist_u + data[xy]
      if alt < dist_v
        queue[v] = alt
        dist[v] = alt
      end
    end
  end
  dist
end

const DIR_STR = ['^', '>', 'v', '<']
function print_path(data::Matrix{Int}, dist::Array{Int, 4}, min_dist::Int, max_dist::Int)
  grid = data .|> (x -> '0' + x)
  print_grid(grid) = foreach(col -> println(prod(col)), eachcol(grid))

  cur = CartesianIndex(argmin(CartesianIndices((1:size(dist, 1), min_dist:max_dist))) do p
    dist[p, size(dist)[3:4]...]
    end, size(dist)[3:4]...)
  while true
    grid[cur[3], cur[4]] = DIR_STR[cur[1]]
    ((cur[3] == 1 && cur[4] == 2) || (cur[3] == 2 && cur[4] == 1)) && break
    prev_pos = CartesianIndex(cur[3], cur[4]) + DIRS[OPPOSITE[cur[1]]]
    if cur[2] != 1
      cur = CartesianIndex(cur[1], cur[2] - 1, prev_pos)
      continue
    end
    min_cost = MAX_COST
    min_alt = CartesianIndex(-1, -1)
    for dir in eachindex(DIRS)
      (dir == cur[1] || dir == OPPOSITE[cur[1]]) && continue
      for i in min_dist:max_dist
        alt = CartesianIndex(dir, i)
        cost = dist[CartesianIndex(alt, prev_pos)]
        if cost < min_cost
          min_alt = alt
          min_cost = cost
        end
      end
    end
    cur = CartesianIndex(min_alt, prev_pos)
  end
  print_grid(grid)
end

data = stack([c - '0' for c in line] for line in eachline())
for (i, (min_dist, max_dist)) in enumerate(((1, 3), (4, 10)))
  dist = dijkstra(data, min_dist, max_dist)
  # print_path(data, dist, min_dist, max_dist)
  println("Part ", i, " ",
    minimum(dist[:, min_dist:max_dist, size(data)...]))
end