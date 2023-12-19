def process_input(filename):
    """Acquire input data"""
    with open(filename) as file:
        input = file.read().splitlines()

    workflows = {}
    parts = []

    for line in input:
        if len(line) == 0: continue

        # Parts
        if line[0] == '{':
            part = line
            for cat in 'xmas':
                part = part.replace(cat+"=", "'"+cat+"':")
            exec('parts.append('+part+')')
            continue

        # Workflows
        line = line.replace('}','')
        token = line.split('{')
        workflow_name = token[0]
        workflow_rules = []
        rules = token[1].split(',')
        for rule in rules[:-1]:
            token = rule.split(':')
            next_workflow = token[1]
            attrib = token[0][0]
            op = token[0][1]
            rating = int(token[0][2:])
            workflow_rules.append((attrib,op,rating,next_workflow))
        workflow_rules.append(('L','=',-1,rules[-1]))
        workflows[workflow_name] = workflow_rules

    return workflows, parts


def check_all_parts():
    accepted = []
    for part in parts:
        result = run_workflow(part)
        if result == 'A':
            accepted.append(part)
    return accepted

def run_workflow(part):
    workflow = 'in'
    while True:
        rules = workflows[workflow]
        for rule in rules:
            workflow = test_rule(part, rule)
            if workflow == '':
                continue
            if workflow in ('A','R'):
                return workflow
            break
    return workflow

def test_rule(part, rule):
    attrib, op, rating, next = rule
    if op == '=':
        return next
    elif op == '<':
        if part[attrib] < rating:
            return next
    elif op == '>':
        if part[attrib] > rating:
            return next
    return ''

def sum_ratings():
    total = 0
    for part in accepted:
        total += sum(part.values())
    return total

#-----------------------------------------------------------------------------------------

filename = 'data.txt'
#filename = 'sample.txt'

workflows, parts = process_input(filename)

accepted = check_all_parts()

total = sum_ratings()

print()
print('Ratings', total)