import cssutils as csu
import sys
import random
from processing import chooseClr

def assignColors(tag, cssObjs, modified, color, modifiedTag):

    #check through each css class for color attribute.
    if(tag.has_attr('class')):        
        stop = False
        for class_nm in tag['class']:            
            if class_nm not in modified:                
                className = "." + class_nm
                for s in cssObjs:
                    for rule in s:                        
                        if rule.type == 1 and rule.selectorText == className:                            
                            for property in rule.style:
                                if property.name == 'color' or property.name == 'background-color' or property.name == 'background':                                    
                                    property.value = color
                                    stop = True                                    
                                    modified.append(className)
                                    break                                
                            if stop == True:
                                break
                    if stop == True:
                        break
            if stop == True:
                break        
    # check through the tags for colors attribute    
    elif(tag.has_attr('style')):    
        print "tag corr.py", tag['style']    
        tmpCss = csu.parseStyle(tag['style'])
        for property in tmpCss:
            if property.name == 'color' or property.name == 'background-color' or property.name == 'background':
                property.value = color
                print "corr.py here", property.name                
            elif property.name == 'font-size':
                #can be exteded to take button specific font, color                
                property.value = str(random.randint(int((property.value).split('p')[0])-2,int((property.value).split('p')[0])+2))+"px"            

        tag['style'] = tmpCss.cssText
        modifiedTag.append(tag)
    return tag, modified, cssObjs, modifiedTag


#generates dark patterns which require more than one css.html elements to be in sync with each other
#e.g misdirection
def genCorrData(htmlSoup, corr_el, modified, cssObjs, modifiedTag, idToColorTable,bckClrList,clrToId, contrastTable):

    #selects a color randomly from background colors list
    i = random.randint(0,len(bckClrList)-1)
    bckClr = bckClrList[i]       

    #selects a color that is related to the background color 
    relatedClrList=[]
    relatedClrList.extend(idToColorTable[clrToId[bckClr]][0])        
    clr = bckClr    

    #to prevent repitition of colors
    usedClrList = []
    usedClrList.append(bckClr)

    #all related css/html elements are assigned different related colors
    for i in range(0, len(corr_el)):        
        strTmp = corr_el[i]                
        tmpTag = htmlSoup.find(id = strTmp)                
        assignColors(tmpTag, cssObjs, modified,clr, modifiedTag)
        usedClrList.append(clr)
        clr = chooseClr(bckClr, usedClrList,relatedClrList)            
    #todo:extension to label as dark pattern or not
