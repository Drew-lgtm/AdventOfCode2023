from collections import defaultdict
from math import prod


modules = dict()
flips = defaultdict(int)
conjs = defaultdict(dict)

for line in open('data.txt'):
    s, _, *ds = line.replace(',', '').split()
    t, s = (s[0], s[1:]) if s[0] in '%&' else ('', s)

    modules[s] = t, ds

    for d in ds:
        conjs[d][s] = 0
        if d == 'rx': rx = s

rx_ins = {i: 0 for i in conjs[rx]}

presses = 0
counts = [0, 0]

while True:
    if presses == 1000:
        print(prod(counts))
    presses += 1

    if all(rx_ins.values()):
        print(prod(rx_ins.values()))
        break

    queue = [(None, 'broadcaster', 0)]
    while queue:
        source, mod, pulse_in = queue.pop(0)
        counts[pulse_in] += 1

        if mod not in modules: continue
        type, nexts = modules[mod]

        match type, pulse_in:
            case '', _:
                pulse_out = pulse_in
            case '%', 0:
                pulse_out = flips[mod] = not flips[mod]
            case '&', _:
                conjs[mod][source] = pulse_in
                pulse_out = not all(conjs[mod].values())

                if 'rx' in nexts:
                    for k, v in conjs[mod].items():
                        if v: rx_ins[k] = presses
            case _,_: continue

        for n in nexts:
            queue.append((mod, n, pulse_out))