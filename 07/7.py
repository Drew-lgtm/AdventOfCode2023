HandList = []
with open("data.txt", "r") as data:
    for t in data:
        Line = t.strip().split()
        A, B = Line
        HandList.append((A, int(B)))

CardDict = {"A": "F", "K": "E", "Q": "D", "J": "C", "T": "B"}
CardSet = {"A", "K", "Q", "J", "T"}
NumHands = len(HandList)

def HandTranslator(RealHand, Part):
    if Part == 2:
        HighCount = 0
        for c in RealHand:
            Count = RealHand.count(c)
            if c == "J" and Count == 5:
                MostCards = "J"
                break
            elif c == "J":
                continue
            if Count > HighCount:
                MostCards = c
                HighCount = Count
        Hand = RealHand.replace("J", MostCards)
    else:
        Hand = RealHand

    HandSet = set(Hand)
    HandLen = len(HandSet)
    if HandLen == 1:
        Type = 7
    elif HandLen == 2:
        Sample = Hand.count(HandSet.pop())
        if Sample == 4 or Sample == 1:
            Type = 6
        else:
            Type = 5
    elif HandLen == 3:
        Sample1 = Hand.count(HandSet.pop())
        Sample2 = Hand.count(HandSet.pop())
        if Sample1 == 2 or Sample2 == 2:
            Type = 3
        else:
            Type = 4
    elif HandLen == 4:
        Type = 2
    else:
        Type = 1
    
    NewHand = RealHand
    for f in CardSet:
        Letter = CardDict[f]
        NewHand = NewHand.replace(f, Letter)
    if Part == 2:
        NewHand = NewHand.replace("C", "1")
    
    return Type, NewHand

Answers = []
for p in range(1,3):
    TranslatedHandList = []
    for Hand, Bid in HandList:
        Type, NewHand = HandTranslator(Hand, p)
        NewTuple = (Type, NewHand, Bid)
        TranslatedHandList.append(NewTuple)

    TranslatedHandList.sort()

    Answer = 0
    for v, a in enumerate(TranslatedHandList):
        Multiple = v + 1
        _, _, Bid = a
        Answer += Multiple * Bid
    Answers.append(Answer)

Part1Answer, Part2Answer = Answers

print(f"{Part1Answer = }")
print(f"{Part2Answer = }")