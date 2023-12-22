import time

starttime = time.time()
filepath = 'data.txt'
advent1file=open(filepath,'r')
listoflines =[[[z for z in y.split(',')] for y in x.strip().split('~')] for x in advent1file.readlines()]

bricks=[]
maxheight=0
for blocks in listoflines:
    x,y,z = blocks[0]
    a,b,c=  blocks[1]
    x=int(x)
    y=int(y)
    z=int(z)
    a=int(a)
    b=int(b)
    c=int(c)
    bot = min(z,c)
    top=max(z,c)
    left=min(x,a)
    right=max(x,a)
    near=min(y,b)
    far=max(y,b)
    bricks.append((bot,top,near,far,left,right))
    maxheight=max(maxheight,top)
    
bricks.sort()
occupied_space=[{} for i in range(maxheight)]
supporting_list=[{} for x in bricks]
i=0
for brick in bricks:
    twodim=[]
    near,far,left,right=brick[2:]
    for y in range(near,far+1):
        for x in range(left,right+1):
            twodim.append((x,y))
    
    curbot=brick[0]
    while curbot-1>=1:
        oktocont=True
        supps=set()
        for dim in twodim:
            if dim in occupied_space[curbot-1].keys():
                oktocont=False
                supps.add(occupied_space[curbot-1][dim])
        supporting_list[i]=supps
        if not oktocont:
            break
        curbot-=1
    top=brick[1]-(brick[0]-curbot)
    for dim in twodim:
        for alt in range(curbot,top+1):
            occupied_space[alt][dim]=i
    i+=1

answer=[True for x in bricks]
for i in supporting_list:
    if len(i)==1:
        for q in i:
            answer[q]=False

answer=[True for x in answer if x == True]
print("part 1")
print(len(answer))    
    
def Falling(supports,brick):
    solid = [x!=brick for x in range(len(supports))]
    extra=0
    oktostop=False
    while not oktostop:
        oktostop=True
        for i in range(len(supports)):
            if len(supports[i])==0:
                continue
            if i==brick or solid[i]==False:
                continue
            if any(solid[x] for x in supports[i]):
                continue
            solid[i]=False
            extra+=1
            oktostop=False
    return extra    

ans=0    
for i in range(len(bricks)):
    ans+=Falling(supporting_list,i)    
print('part 2')    
print(ans)
print(time.time()-starttime)
