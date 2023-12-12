# Puzzle:            https://adventofcode.com/2023/day/12
# Video explanation: https://youtu.be/WiNz_zBhGIM

# 1. part - What is the sum of possible arrangements?
def arrangement_count(p, g, springs, groups):
    if g >= len(groups): # no more groups
        if p < len(springs) and '#' in springs[p:]:
            # eg: .##?????#.. 4,1
            return 0 # not a solution - there are still damaged springs in the record
        return 1
    
    if p >= len(springs):
        return 0 # we ran out of springs but there are still groups to arrange

    res = None
    gs = groups[g] # damaged group size

    if springs[p] == '?':
        # if we can start group of damaged springs here
        # eg: '??#...... 3' we can place 3 '#' and there is '?' or '.' after the group
        # eg: '??##...... 3' we cannot place 3 '#' here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            # start damaged group here + this spring is operational ('.')
            res = arrangement_count(p + gs + 1, g + 1, springs, groups) + arrangement_count(p + 1, g, springs, groups)
        else:
            # this spring is operational ('.')
            res = arrangement_count(p + 1, g, springs, groups)
    elif springs[p] == '#':
        # if we can start damaged group here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            res = arrangement_count(p + gs + 1, g + 1, springs, groups)
        else:
            res = 0 # not a solution - we must always start damaged group here
    elif springs[p] == '.':
        res = arrangement_count(p+1, g, springs, groups) # operational spring -> go to the next spring

    return res

with open('data.txt') as f:
    sum_of_arrangements = 0

    for line in f.readlines():
        springs, groups = line.split()

        groups = list(map(int, groups.split(',')))
        springs = springs + '.' # make sure there is operational spring after each damaged group

        sum_of_arrangements += arrangement_count(0, 0, springs, groups)

    print(sum_of_arrangements)

# 2. part - What is the sum of possible arrangements with unfolded records?
MEMO = {} # <-- change here

def arrangement_count(p, g, springs, groups):
    if g >= len(groups): # no more groups
        if p < len(springs) and '#' in springs[p:]:
            # eg: .##?????#.. 4,1
            return 0 # not a solution - there are still damaged springs in the record
        return 1
    
    if p >= len(springs):
        return 0 # we ran out of springs but there are still groups to arrange

    if (p, g) in MEMO: return MEMO[(p, g)] # <-- change here

    res = None
    gs = groups[g] # damaged group size

    if springs[p] == '?':
        # if we can start group of damaged springs here
        # eg: '??#...... 3' we can place 3 '#' and there is '?' or '.' after the group
        # eg: '??##...... 3' we cannot place 3 '#' here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            # start damaged group here + this spring is operational ('.')
            res = arrangement_count(p + gs + 1, g + 1, springs, groups) + arrangement_count(p + 1, g, springs, groups)
        else:
            # this spring is operational ('.')
            res = arrangement_count(p + 1, g, springs, groups)
    elif springs[p] == '#':
        # if we can start damaged group here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            res = arrangement_count(p + gs + 1, g + 1, springs, groups)
        else:
            res = 0 # not a solution - we must always start damaged group here
    elif springs[p] == '.':
        res = arrangement_count(p+1, g, springs, groups) # operational spring -> go to the next spring

    MEMO[(p, g)] = res # <-- change here
    return res

with open('data.txt') as f:
    sum_of_arrangements = 0

    for line in f.readlines():
        springs, groups = line.split()
       
        springs = "?".join([springs] * 5)
        springs = springs + '.' # add extra operational spring
        groups = list(map(int, groups.split(','))) * 5

        MEMO = {} # don't forget to clear MEMO
        sum_of_arrangements += arrangement_count(0, 0, springs, groups)

    print(sum_of_arrangements)

# 1. and 2. part combined
MEMO = {}

def arrangement_count(p, g, springs, groups):
    if g >= len(groups): # no more groups
        if p < len(springs) and '#' in springs[p:]:
            # eg: .##?????#.. 4,1
            return 0 # not a solution - there are still damaged springs in the record
        return 1
    
    if p >= len(springs):
        return 0 # we ran out of springs but there are still groups to arrange

    if (p, g) in MEMO: return MEMO[(p, g)]

    res = None
    gs = groups[g] # damaged group size

    if springs[p] == '?':
        # if we can start group of damaged springs here
        # eg: '??#...... 3' we can place 3 '#' and there is '?' or '.' after the group
        # eg: '??##...... 3' we cannot place 3 '#' here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            # start damaged group here + this spring is operational ('.')
            res = arrangement_count(p + gs + 1, g + 1, springs, groups) + arrangement_count(p + 1, g, springs, groups)
        else:
            # this spring is operational ('.')
            res = arrangement_count(p + 1, g, springs, groups)
    elif springs[p] == '#':
        # if we can start damaged group here
        if '.' not in springs[p:p + gs] and springs[p + gs] != '#':
            res = arrangement_count(p + gs + 1, g + 1, springs, groups)
        else:
            res = 0 # not a solution - we must always start damaged group here
    elif springs[p] == '.':
        res = arrangement_count(p+1, g, springs, groups) # operational spring -> go to the next spring

    MEMO[(p, g)] = res
    return res

with open('data.txt') as f:
    lines = f.readlines()

    for repetitions in [1, 5]:
        sum_of_arrangements = 0

        for line in lines:
            springs, groups = line.split()
        
            springs = "?".join([springs] * repetitions)
            springs = springs + '.' # add extra operational spring
            groups = list(map(int, groups.split(','))) * repetitions

            MEMO = {} # don't forget to clear MEMO
            sum_of_arrangements += arrangement_count(0, 0, springs, groups)

        print(sum_of_arrangements)