with open("data.txt", "r") as f:
  parts = f.read().split("\n\n")
  rules = parts[0].splitlines()

processed_rules = {}
for rule in rules:
  name, matches = rule.split("{")
  matches = matches.split("}")[0]
  matches = matches.split(",")
  processed_rules[name] = []
  for match in matches:
    parts = match.split(":")
    if len(parts) == 2:
      processed_rules[name].append((parts[0], parts[1]))
    else:
      processed_rules[name].append(("True", parts[0]))
  print(f"{name}: {processed_rules[name]}")

def process_criteria(criteria):
  vals = {
    "x": [0] + [1] * 4000,
    "m": [0] + [1] * 4000,
    "a": [0] + [1] * 4000,
    "s": [0] + [1] * 4000,
  }
  for c in criteria:
    if c != "True":
      if c[0] == "!":
        c = c[1:]
        var, c, limit = c[0], c[1], int(c[2:])
        if c == "<": # >= limit is okay
          for i in range(1, limit):
            vals[var][i] = 0
        else: # <= limit is okay
          for i in range(limit + 1, 4001):
            vals[var][i] = 0
      else:
        var, c, limit = c[0], c[1], int(c[2:])
        if c == "<": # < limit is okay
          for i in range(limit, 4001):
            vals[var][i] = 0
        else: # > limit is okay
          for i in range(1, limit + 1):
            vals[var][i] = 0
  subtotal = 1
  for var, valid in vals.items():
    print(f"{var}: {sum(valid)}")
    subtotal *= sum(valid)
  return subtotal

def process_rule(name, previous_crit, previous_rules):
  total = 0
  inverted_criteria = []
  for criteria, rule in processed_rules[name]:
    if rule == "A":
      print(f"{previous_rules + [name]}: {previous_crit + inverted_criteria + [criteria]}")
      total += process_criteria(previous_crit + inverted_criteria + [criteria])
      inverted_criteria += ["!" + criteria]
    else:
      if rule != "R":
        total += process_rule(rule, previous_crit + inverted_criteria + [criteria], previous_rules + [name])
      inverted_criteria += ["!" + criteria]
  return total
      
print(process_rule("in", [], []))
