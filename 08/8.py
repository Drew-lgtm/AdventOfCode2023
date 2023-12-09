#Parse Input
directions = []
nodes = {}
currNodes = []
with open('data.txt', 'r') as file:
    for line in file:
        if directions == []: 
            directions = line.replace('\n', '')
        elif line != '\n':
            nodes[line[0:3]] = (line[7:10], line[12:15])
            if line[2] == 'A': currNodes.append(line[0:3])


#Part 1
currNode = 'AAA'
steps = 0
while currNode != 'ZZZ':
    currDir = directions[steps % len(directions)]
    if currDir == 'L':
        currNode = nodes[currNode][0]
    elif currDir == 'R':
        currNode = nodes[currNode][1]
    steps += 1

print('Part 1:', steps)


#Part 2
steps = [0] * len(currNodes)
for cn in range(len(currNodes)):
    currNode = currNodes[cn]

    while currNode[2] != 'Z':
        currDir = directions[steps[cn] % len(directions)]
        if currDir == 'L':
            currNode = nodes[currNode][0]
        elif currDir == 'R':
            currNode = nodes[currNode][1]
        steps[cn] += 1

#Find LCM of all steps
for s in range(len(steps)-1):
    greater = max(steps[s], steps[s+1])
    currMul = greater

    while (currMul % steps[s] != 0 or currMul % steps[s+1] != 0):
        currMul += greater
    
    steps[s+1] = currMul

print('Part 2:', steps[len(steps)-1])
