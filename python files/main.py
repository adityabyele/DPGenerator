from bs4 import BeautifulSoup
from corr import genCorrData
from preSel import genCombinations
from processing import init
import cssutils as csu
import fnmatch
import os


#return a list of css objects and return
def getCssObjects(soup, dir_name):    
    cssObjList = []
    fname=None
    cssDict={}
    styleTagList=[]
    #if there is a link get the object from the file and link
    linkTag = soup.link
    if linkTag != None:
        if(linkTag.has_attr('rel') and  ("stylesheet" in linkTag['rel'])):
            if linkTag.has_attr('href'):                
                fname = linkTag['href']
                cssObj = csu.parseFile(filename=dir_name+"/"+fname)                 
                cssDict[cssObj] = fname
                cssObjList.append(cssObj)    
        #todo:extend for multiple link tags                
    #if it is in style tag            
    styleTag = soup.style
    if styleTag != None:
        cssStyleObj = csu.parseString(styleTag.string)            
        cssObjList.append(cssStyleObj)
        styleTagList.append(cssStyleObj)
        #todo:extend for multiple style tags
    return cssObjList, cssDict, styleTagList


def generateHtml(soup, count, dir_name, corr_el,idToColorTable,bckClrList,clrToId, contrastTable):    
    #get a list cssutils objects
    cssObjs, cssDict, styleTagList = getCssObjects(soup, dir_name)    
    modified = []
    modifiedTag=[]
    #check for the existence of correlated attributes
    if(len(corr_el) > 1):
        genCorrData(soup, corr_el, modified, cssObjs, modifiedTag,idToColorTable,bckClrList,clrToId, contrastTable)        

    #if the html contains checkboxes or radio buttons mark them in all possible combinations and create a html file for each (e.g preselected options)   
    return genCombinations(soup,cssObjs, modified, modifiedTag, cssDict, styleTagList, count,idToColorTable,bckClrList,clrToId, contrastTable)            

if __name__ == '__main__':
    #todo: argparse take file name
    direc = "../data/"
    exclude = []
    fileList = []

    #path to files where data is stored.
    ################################################
    # todo:make config file    
    countFile = "../output/count.txt"    
    #seed/template web pages stored here
    dataDir = "../data/"
    #comma separated ids of dark patterns that are related(e.g background/foreground color matching)
    #in a seed/template webpage. 
    corrFile = "/corr.txt"
    ###############################################

    # traverse each level and get files in each dir
    for root, dirs, files in os.walk('../data/', topdown=True):        
        for name in files:            
            if fnmatch.fnmatch(name, '*.html'):
                dirname = root.split(os.path.sep)[-1]                
                fileList.append(dirname+"/"+name)                

    #get the current count of files            
    with open(countFile) as fpCount:
        content = fpCount.readlines()
        content = [x.strip() for x in content]
    count = int(content[0])

    #get colors
    idToColorTable,bckClrList,clrToId, contrastTable = init()
            
    for fName in fileList:
        fileName = dataDir + fName
        fPath = fileName.rsplit('/',1)[0]    

        ####################################################################        
        #process each template
        with open(fileName) as fp:
            soup = BeautifulSoup(fp,"lxml")     
        corr_el=[]
        if os.path.isfile(fPath+corrFile):
            with open(fPath+corrFile) as fp1:
                content = fp1.readlines()
                content = [x.strip() for x in content]
                corr_el= content[0].split(',')
        #generate html from this html
        for i in range(0,20):
            count=generateHtml(soup,count, fileName.rsplit('/',1)[0], corr_el,idToColorTable,bckClrList,clrToId, contrastTable)            
        ########################################################################

    with open(countFile,"w") as fpCount:
        fpCount.write(str(count))