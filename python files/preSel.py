import bs4
import cssutils as csu
import random
import os
import sys

#write to file
def writeToFile(soup, cssObjs, cssDict, styleTagList, count):
    if not os.path.exists("../output/"+str(count)):
        os.makedirs("../output/"+str(count))
    for cssOb in cssObjs:
        if(cssOb in cssDict):
            cssFName = cssDict[cssOb]            
            with open("../output/"+str(count)+"/"+cssFName, "w") as file:
                file.write(cssOb.cssText)
        elif(cssOb in styleTagList):
            soup.style.string = cssOb.cssText            
                    
    with open("../output/"+str(count)+"/"+str(count)+".html", "w") as file:
        file.write(str(soup))


def genCombinations(htmlSoup, cssObjs, modified, modifiedTag,  cssDict, styleTagList, count, idToColorTable,bckClrList,clrToId, contrastTable):    
    inputTags = htmlSoup.findAll('input')    
    chkBoxList = []    

    #reset all checkboxes
    if len(inputTags) != 0:        
        chkBoxList = [ tag for tag in inputTags if tag['type'] == 'checkbox']    
    strB = '{0:0'+str(len(chkBoxList))+'b}'    
    for j in range(0, len(chkBoxList)):
        if(chkBoxList[j].has_attr('checked')):
                del chkBoxList[j]['checked']                
    
    #output all combinations of checkboxes
    for i in range(0, 2**len(chkBoxList)):        
        strTmp = strB.format(i)
        char_list = [x for x in strTmp]
        for j in range(0, len(chkBoxList)):
            if(char_list[j] == '0' and chkBoxList[j].has_attr('checked')):
                del chkBoxList[j]['checked']
            elif(char_list[j] == '1' and not chkBoxList[j].has_attr('checked')):
                chkBoxList[j]['checked'] = ""
        # assign colors to non-dark pattern elements
        assnColors(htmlSoup, cssObjs, modified, modifiedTag,idToColorTable,bckClrList,clrToId, contrastTable)
        count=count+1
        writeToFile(htmlSoup, cssObjs, cssDict, styleTagList, count)                    
    return count
    

def assnColors(htmlSoup, cssObjs, modified, modifiedTag, idToColorTable,bckClrList,clrToId, contrastTable):    
    num=-1
    #################################################################
    #selects a color randomly from background colors list
    i = random.randint(0,len(bckClrList)-1)    
    bckClr = bckClrList[i]        
    relatedClrList=[]

    #select contradictory color because this type of dark pattern doesnt require related colors/elements 
    k = clrToId[bckClr]    
    j = contrastTable[k]    
    
    relatedClrList.extend(idToColorTable[clrToId[bckClr]][0])    
    complClrList=[]
    complClrList.extend(idToColorTable[j][0])    
    ################################################################

    for obj in cssObjs:   
        i = random.randint(0,len(bckClrList)-1)    
        for rule in obj:            
            if rule.type == 1 and (rule.selectorText not in modified):                
                #select the class with the desired classname
                #randomly change attribute properties                
                num = random.randint(0,len(relatedClrList)-1)
                bckClr = relatedClrList[num]                
                for property in rule.style:                
                    if property.name == 'color':                        
                        num = random.randint(0,len(complClrList)-1)
                        property.value = complClrList[num]
                    elif property.name == 'background-color':                        
                        t = random.randint(0,len(complClrList)-1)
                        property.value = bckClrList[t]                        
                    elif property.name == 'font-size' 
                        #can be extended to take button specific font, color
                        property.value = str(random.randint(int((property.value).split('p')[0])-2,int((property.value).split('p')[0])+2))+"px"                        
    
    #iter over all css objects along with modified and tmpmodified
    #iterate over tags and check for inline styling
    for child in htmlSoup.descendants:        
        if(isinstance(child, bs4.element.Tag) and child.has_attr('style')) and child not in modifiedTag:            
            tmpCss = csu.parseStyle(child['style'])
            r = lambda: random.randint(0,255)
            for property in tmpCss:                
                if property.name == 'color':                    
                    num = random.randint(0,len(complClrList)-1)
                    property.value = complClrList[num]
                elif property.name == 'background-color':
                    num = random.randint(0,len(complClrList)-1)
                    property.value = complClrList[num]                                        
                elif property.name == 'font-size':
                        #can be exteded to take button specific font, color
                        property.value = str(random.randint(int((property.value).split('p')[0])-2,int((property.value).split('p')[0])+2))+"px"                        
            child['style'] = tmpCss.cssText              