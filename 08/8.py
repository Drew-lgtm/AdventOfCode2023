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