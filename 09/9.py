part1, part2 = 0, 0
for line in open("data.txt").readlines():
    l = [[int(x) for x in line.split()]]
    for seq in l:
        diff = [x-seq[i-1] for i, x in enumerate(seq) if i != 0]
        l.append(diff)
        if not any(diff):
            break
    for i, seq in enumerate(l[::-1], 1):
        if len(l) - i != 0:
            # part 1
            l[-i-1].append(seq[-1]+l[-i -1][-1])
            # part 2
            l[-i-1].insert(0,l[-i -1][0]-seq[0])
    part1 += l[0][-1]
    part2 += l[0][0]    
print("Part 1:", part1)
print("Part 2:", part2)