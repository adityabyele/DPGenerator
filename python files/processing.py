from bs4 import BeautifulSoup
from collections import defaultdict
import cssutils as csu
import random
def getColors(colorFile):
    #get bck colors    
    with open(colorFile) as bf:
            bcSoup = BeautifulSoup(bf,"lxml")     
    tgList = bcSoup.find_all('h1')
    clrList=[]
    for hTag in tgList:        
         tmpStr = hTag['style']
         tmpStr = tmpStr.split(':')[1]
         tmpStr = tmpStr.rsplit(';',1)[0]
         clrList.extend(tmpStr.split(','))         
    return clrList

#returns colors that are similar, colors that are contrasting
# colors commonly used as background colors.
def init():
    #todo:get from config
    colorFile = "../colorSet/relatedColors.html"
    bckColorsFile = "../colorSet/bckColors.txt"    
    contrastingSetFile = "../colorSet/contrastingSet.txt"    
    idToColorTable = getColorSet(colorFile)
    bckClrList, clrToId = getbckColors(bckColorsFile)    
    contrastTable = getContrastColors(contrastingSetFile)    
    return idToColorTable,bckClrList,clrToId, contrastTable

    
#matches each color to its set id
def getColorSet(colorFile):
    with open(colorFile) as bf:
            bcSoup = BeautifulSoup(bf,"lxml")     
    tgList = bcSoup.find_all('h1')    
    idToColor = defaultdict(list)
    for hTag in tgList:        
         tmpStr = hTag['style']
         tmpStr = tmpStr.split(':')[1]
         tmpStr = tmpStr.rsplit(';',1)[0]         
         idToColor[int(hTag['id'])].append(tmpStr.split(','))             
    return idToColor

#returns a list of background colors along with a mapping of which color elongs to  which id    
def getbckColors(bckColorsFile):
    with open(bckColorsFile) as fp:
        content = fp.readlines()        
    content = [x.strip() for x in content] 
    clrToId = {}
    bckClrList = []
    for ln in content:
        a,b = ln.split(',')
        clrToId[b] = int(a)        
        bckClrList.append(b)
    return bckClrList, clrToId

# returns contrasting colors mapped to their id
def getContrastColors(contrastingSetFile):
    with open(contrastingSetFile) as fp:
        content = fp.readlines()        
    content = [x.strip() for x in content]     
    contrastTable = {}    
    for ln in content:
        a,b = ln.split(',')
        contrastTable[int(a)] = int(b)        
    return contrastTable

def chooseClr(bckClr,usedClrList,relatedClrList):    
    clr = relatedClrList[random.randint(0, len(relatedClrList)-1)]    
    while(clr == bckClr):        
            clr = relatedClrList[random.randint(0, len(relatedClrList)-1)]
    return clr