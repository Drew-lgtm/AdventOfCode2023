InputList = []
with open("data.txt", "r") as data:
    for t in data:
        Line = t.strip()
        InputList.append(Line)

OpenSet = set()
RockSet = set()
for y, i in enumerate(InputList):
    for x, c in enumerate(i):
        Loc = (x,y)
        if c == "#":
            RockSet.add(Loc)
        elif c == ".":
            OpenSet.add(Loc)
        elif c == "S":
            OpenSet.add(Loc)
            StartPoint = Loc


Directions = [(0,1),(1,0),(0,-1),(-1,0)]

def WalkGrid(StartPoint, Limit):
    EvenSet = set()
    OddSet = set()
    QueueSet = set()
    QueueSet.add(StartPoint)
    Steps = 0
    while True:
        Steps += 1
        Moved = False
        if Steps%2 == 0:
            OldSet = EvenSet
        else:
            OldSet = OddSet
        NewQueueSet = set()
        for x, y in QueueSet:
            for DX,DY in Directions:
                NX,NY = x+DX,y+DY
                NewLoc = (NX,NY)
                if NewLoc in RockSet or NewLoc in OldSet or NewLoc not in OpenSet:
                    continue
                NewQueueSet.add(NewLoc)
                OldSet.add(NewLoc)
                Moved = True
        QueueSet = NewQueueSet.copy()
        if (Limit != None and Steps == Limit) or not(Moved):
            break
    
    if Limit == None:
        return len(OddSet), len(EvenSet)
    elif Limit%2 == 1:
        return len(OddSet)
    else:
        return len(EvenSet)

Part1Answer = WalkGrid(StartPoint, 64)


Height = len(InputList)
Width = len(InputList[0])
StartX, StartY = StartPoint
FullGridOdd, FullGridEven = WalkGrid(StartPoint, None)
NorthStart = (StartX, Height-1)
SouthStart = (StartX, 0)
WestStart = (Width-1,StartY)
EastStart = (0,StartY)
NWStart = (Width-1,Height-1)
NEStart = (0,Height-1)
SWStart = (Width-1,0)
SEStart = (0,0)
#26501365
#AssumptionMade, startpoint is in exact center of grid and the grid has veins dividing the grid into four by open points

Radius = 26501365//Height
DiagLimit1 = (26501365-StartX-StartY-2)%(Height+Width)
DiagLimit2 = (26501365-StartX-StartY-Height-2)%(Height+Width)
CardLimit = (26501365-StartX-1)%Height
OddGrids = 1
EvenGrids = 0
for t in range(Radius):
    Num = t-1
    if Num%2==0:
        EvenGrids += t*4
    else:
        OddGrids += t*4

NorthGridNum = WalkGrid(NorthStart, CardLimit)
SouthGridNum = WalkGrid(SouthStart, CardLimit)
WestGridNum = WalkGrid(WestStart, CardLimit)
EastGridNum = WalkGrid(EastStart, CardLimit)

NWGrid1 = WalkGrid(NWStart,DiagLimit1)
NEGrid1 = WalkGrid(NEStart,DiagLimit1)
SWGrid1 = WalkGrid(SWStart,DiagLimit1)
SEGrid1 = WalkGrid(SEStart,DiagLimit1)
NWGrid2 = WalkGrid(NWStart,DiagLimit2)
NEGrid2 = WalkGrid(NEStart,DiagLimit2)
SWGrid2 = WalkGrid(SWStart,DiagLimit2)
SEGrid2 = WalkGrid(SEStart,DiagLimit2)


FullGridTotal = OddGrids*FullGridOdd + EvenGrids*FullGridEven
DiagsTotal = (NWGrid1+NEGrid1+SEGrid1+SWGrid1)*(Radius-1) + (NWGrid2+NEGrid2+SEGrid2+SWGrid2)*Radius
CardsTotal = NorthGridNum+SouthGridNum+EastGridNum+WestGridNum
Part2Answer = FullGridTotal + DiagsTotal + CardsTotal

print(f"{Part1Answer = }")
print(f"{Part2Answer = }")