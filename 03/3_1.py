import os
import math

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

text =  open_file(os.path.join(os.path.dirname(__file__), 'data.txt'))
test = open_file(os.path.join(os.path.dirname(__file__), 'data2.txt'))

def formatInput(text):
    textArr = text.split('\n')
    textMat =[]  
    for i in range(len(textArr)):
        rowArr = list(textArr[i])
        textMat.append(rowArr)
    return textMat


nums = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']

def getNeighbors(mat, row, colStart, colEnd):
    neighbors = []
    rowLen = len(mat)
    colLen = len(mat[0])
    leftAvailable = False
    rightAvailable = False
    # same row - left
    if colStart-1 >=0:
        leftAvailable = True
        neighbors.append(mat[row][colStart-1])
    # same row - right
    if colEnd+1 < colLen:
        rightAvailable = True
        neighbors.append(mat[row][colEnd+1])
    # upper row
    if row-1 >=0:
        #upper row -left
        if leftAvailable:
            neighbors.append(mat[row-1][colStart-1])
        #upper row -right
        if rightAvailable:
            neighbors.append(mat[row-1][colEnd+1])
        #upper row -middle
        neighbors.extend(mat[row-1][colStart:colEnd+1])
    # lower row
    if row+1 < rowLen:
        #lower row -left
        if leftAvailable:
            neighbors.append(mat[row+1][colStart-1])
        #lower row -right
        if rightAvailable:
            neighbors.append(mat[row+1][colEnd+1])
        #lower row -middle
        neighbors.extend(mat[row+1][colStart:colEnd+1])
    return neighbors

def getWholeNumber(row, currCol):

    num = ''
    for i in range(currCol, len(row)):
        if row[i] in nums:
            num += row[i]
        else:
            break
    return num, len(num)
def getSumPartNumbers(mat):
    sumPartNumbers = 0
    rowLen = len(mat)
    colLen = len(mat[0])
    for i in range(rowLen):
        skip=0
        for j in range(colLen):
            if skip > 0:
                skip -= 1
                continue
            if mat[i][j] in nums:

                num, numLen = getWholeNumber(mat[i], j)

                skip = numLen-1
                neighbors = getNeighbors(mat, i,j, j+numLen-1)
                isPartNumber = False
                for k in range(len(neighbors)):
                    if neighbors[k] !='.':
                        if neighbors[k] not in nums:
                            isPartNumber = True
                            break
                if isPartNumber:
                    sumPartNumbers += int(num)
    return sumPartNumbers
print(getSumPartNumbers(formatInput(text)))
