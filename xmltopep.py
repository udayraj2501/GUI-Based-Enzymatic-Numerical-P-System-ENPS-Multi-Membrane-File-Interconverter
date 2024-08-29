import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]


import xml.etree.ElementTree as ET


it = ET.iterparse(arguments[0])
for _, el in it:
    el.tag = el.tag.split('}', 1)[1]
root = it.root

stackName = []
stackAddress = []
stackAttrib = []
temp = root.iter()
for elt in temp:
    if((elt.tag == 'region' or elt.tag == 'membrane' or elt.tag == 'children') and len(list(elt)) != 0 ):
        stackName.append(elt.tag)
        stackAddress.append(elt)
        stackAttrib.append(elt.attrib)    

completed= []
for i in range(len(stackName)):
    completed.append(False)
def structure():
    stringTemp = ''
    for i in range(len(stackName),-1,-1):
       if(not(completed[i-1])): 
            if(stackName[i-1] == 'region'):
                completed[i-1] = True
                continue
            elif(stackName[i-1] == 'membrane'):
                completed[i-1] = True
                temp = str(stackAttrib[i-1]['name'])
                stringTemp = f"[{temp} ] {temp} {stringTemp}"
            else:
                tempIndex = i-1
                while(stackName[tempIndex] != 'membrane'):
                    tempIndex -= 1
                completed[tempIndex] = True
                temp = stackAttrib[tempIndex]['name']
                stringTemp = f"[{temp} {stringTemp} ]{temp}"
    return stringTemp
k = structure() 
structureF=k


variables = []
variablesAddress=[]
regionAddress = []
variables
for i in range(0,len(stackName)):
    if(stackName[i] == 'region'):
        variables.append([])
        variablesAddress.append([])
        regionAddress.append(stackAddress[i])
        
for i in range(0,len(regionAddress)):
    memory = regionAddress[i].find('memory')
    memoryIterator = memory.iter()
    for child in memoryIterator:
        if(child.tag == 'memory'):
            continue
        variables[i].append(child.text)
        variablesAddress[i].append(child)




def isEnzyme(inputString):
    return ('stop' in inputString.attrib.keys())
                
variableString = []
for i in range(0,len(variables)):
    variableString.append('var = { ')

    
for i in range(0,len(variables)):
    variableString[i] += (",".join(string.text for string in variablesAddress[i] if not isEnzyme(string))) + '}'    

enzymeNames = []
noOfMembranes = 0;
for i in range(0,len(stackName)):
    if(stackName[i] == 'membrane'):
        noOfMembranes += 1
        
for i in range(0,noOfMembranes):
    enzymeNames.append([])
    
counter = 0
for i in range(0,len(stackAddress)):
    if(stackName[i] == 'region' ):
        
        temp = stackAddress[i].iter()
        
        for child in temp:
            if(child.tag == 'enzyme'):
                enzymeNames[counter].append(child.text) 
        counter += 1

enzymeSet = []
for i in range(0,len(enzymeNames)):
    enzymeSet.append([])
    
for i in range(0,len(enzymeSet)):
    enzymeSet[i].extend(set(enzymeNames[i]))


enzymeString = []
for i in range(0,len(variables)):
    enzymeString.append('E = {')
    
for i in range(0,len(variables)):
    enzymeString[i] += (",".join(string.text for string in variablesAddress[i] if isEnzyme(string))) + '}'


varInitialValues = []
for i in  range(0,len(regionAddress)):
    varInitialValues.append([])

for i in range(0,len(regionAddress)):
    memory = regionAddress[i].find('memory')
    memoryIterator = memory.iter()
    for child in memoryIterator:
        if(child.tag == 'memory'):
            continue
#         if('input' in child.attrib.keys()):
        varInitialValues[i].append(child.attrib['initialValue'])

varInitialValueString = []
varInitialValues=[]
enzymeInitialValueString=[]
for i in range(0,len(variables)):
    varInitialValueString.append('var = {')
    enzymeInitialValueString.append('E0 = (')
    varInitialValues.append('var0 = (')
for i in range(0,len(variables)):
    varInitialValueString[i] += (", ".join(string.text for string in variablesAddress[i] if not isEnzyme(string))) + '}'
    varInitialValues[i] += (", ".join(string.attrib['initialValue'] for string in variablesAddress[i] if not isEnzyme(string))) + ")"

for i in range(0,len(variables)):    
#     enzymeInitialValueString[i] = enzymeInitialValueString[i][:-1] + ")"
    enzymeInitialValueString[i] += (",".join(string.attrib['initialValue'] for string in variablesAddress[i] if isEnzyme(string))) + ")"
        
stackAttrib
memNames=[]
for i in range(0,len(stackAttrib)):
    if(bool(stackAttrib[i])):
        memNames.append(stackAttrib[i]['name'])
memNames
memString = ",".join(memNames)


RPAddress = []
for i in range(0,len(stackAddress)):
    if(stackName[i] == 'region'):
        RPAddress.append([])
        
counter=-1
for i in range(0,len(stackAddress)):
    if(stackName[i] == 'region'):
        temp = stackAddress[i].iter()
        counter+=1
        for child in temp:
            if(child.tag == "repartitionProtocol"):
                RPAddress[counter].append(child)
         

repartitionVariables =[]
repartitionVariablesValues=[]
for i in range(0,len(RPAddress)):
    repartitionVariables.append([])
    repartitionVariablesValues.append([])
    for j in range(0,len(RPAddress[i])):
        repartitionVariables[i].append([])
        repartitionVariablesValues[i].append([])
        
for i in range(0,len(RPAddress)):
    for j in range(0,len(RPAddress[i])):
        temp = RPAddress[i][j].iter()
#         print(RPAddress[i][j])
        for child in temp:
            if(child.tag == "repartitionProtocol"):
                continue
#             print(child)
            repartitionVariables[i][j].append(child.text)
#             print(child.attrib['contribution'])
            repartitionVariablesValues[i][j].append(child.attrib['contribution'])

appended=[]

for i in range(0,len(RPAddress)):
    appended.append([])
    for j in range(0,len(RPAddress[i])):
        appended[i].append([])


for i in range(0,len(repartitionVariables)):
    for j in range(0,len(repartitionVariables[i])):
        for k in range(0,len(repartitionVariables[i][j])):
            appended[i][j].append(repartitionVariablesValues[i][j][k]+"|"+repartitionVariables[i][j][k])


repartitionString = [] 
for i in range(0,len(repartitionVariables)):
    repartitionString.append([])
repartitionString

for i in range(0,len(repartitionVariables)):
    for j in range(0,len(repartitionVariables[i])):
        repartitionString[i].append(" + ".join(string for string in appended[i][j])) 
            


PFEnzyme=[]
for i in range(0,len(RPAddress)):
    PFEnzyme.append([])
    for j in range(0,len(RPAddress[i])):
        PFEnzyme[i].append([])

rules = []
for i in range(0,len(stackAddress)):
    if(stackName[i] == 'region'):
        rules.append([])

counter=-1
for i in range(0,len(stackAddress)):
    if(stackName[i] == 'region'):
        temp = stackAddress[i].iter()
        counter+=1
        for child in temp:
            if(child.tag == "rule"):
                rules[counter].append(child)

for i in range(0,len(rules)):
    for j in range(0,len(rules[i])):
        temp = rules[i][j].iter()
        
        for child in temp:
#             print(child)
            if(child.tag == "rule"):
                continue
            if(child.tag == 'enzyme'):
                PFEnzyme[i][j].append(child.text)
                continue

def mathmlToExp(xml):
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    global c
    c=[]
    l= ""
    
    def calls(value):
#         global c
        if (value.tag == "apply"):
#             print ("(")
            c.append ("(")
            for values in value:
                calls (values)

            c.append (")")
#             print (")")

        else:
            if (value.tag == "ci" or value.tag == "cn"):
    # 			print (value.text) 
                c.append (value.text)
            if (value.tag == "times"):
    # 			print ("*")
                c.append ("*")
            if (value.tag =="pow"):
    # 			print ("^")
                c.append ("^")
            if (value.tag =="add"):
    # 			print ("+")
                c.append ("+")	
            if (value.tag =="minus"):
    # 			print ("-")
                c.append ("-")		
            if (value.tag =="div"):
    #             print("/")
                c.append("/")

    for values in root:
        calls (values)
    i=0

    if(len(root)==0):
        return root.text

    c.insert(0,'(')
    c.append(')')
    z=c

    no = z.count('(') - 1
    order=[]
    def find_nth(haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    counter = 0

    if(z[-2] == ")"):
        pre1 = "first"
    else:
        pre1 = "second"

    while(len(z)!= 0):
#         print(z)
        startI = len(z) -1 - z[::-1].index('(')
        endI = z.index(')')
#         print(startI-1)

        if(z[startI-1] in ['/','*','-','+','^']):
            order.insert(0,"first")
        else:
            order.insert(0,"second")
        z = z[:startI] + z[endI+1:]

    order[0] = pre1
    
    
    
    d =c

    start = len(d) - 1 - d[::-1].index('(')
    end=d.index(")")
    li = []
    string='('

    while(len(d)!=0):    
        length = len(d)
    #     print(d)
        start = len(d) - 1 - d[::-1].index('(')
        end=d.index(")")

        flag = 0
        if(start !=0):
            if(d[start-1] in ['/','*','-','+','^']):
                flag = 1
    #     print("flag:" + str(flag))
    #         print(li)
    #         print(start,end)
        if(end == start + 3):
            string += d[start+1]
            string += d[end-1]
    #             print("if"+d[start+1])

            li.insert(0,string)
            string=""
        else:    
            string = (d[start+1].join(x for x in d[start+2:end]))
            string = '(' + f"{string}" + ')'
            li.insert(0,string)
            string=""

        d = d[:start] + d[end+1:]

    while(len(li) > 1 and len(order)>0):
        tempstr=""
        if(order[-1] == 'first'):
            op1 = li.pop()
            order.pop()
            if(op1[0] in ['/','*','-','+','^'] and order[-1] == "first"):
                op1 = op1[1:] + op1[0]
            op2 = li.pop()

            if(op2[0] in ['/','*','-','+','^'] and order[-1] == "first"):
                op2 = op2[1:] + op2[0]
            order.pop()
            tempstr = op1 + op2
#             print(tempstr)
            li.append(tempstr)
            if(len(order)>0):
                if(order[-1] == "first" ):
                    order.append("second")
                else:
                    order.append("first")

        else:
            op2 = li.pop()

            if(op2[0] in ['/','*','-','+','^'] and order[-1] == "first"):
                op2 = op2[1:] + op2[0]
            order.pop()
            op1 = li.pop()

            if(op1[0] in ['/','*','-','+','^'] and order[-1] == "first"):
                op1 = op1[1:] + op1[0]
            order.pop()
            tempstr = op1+op2
#             print(tempstr)
            li.append(tempstr)
            if(len(order) > 0):
                if(order[-1] == "first" ):
                    order.append("second")
                else:
                    order.append("first")

    return(li[0])

f= open(arguments[0],'r')
abc= f.read()
abc.replace('\n','').replace('\t','').replace('  ','')

import re

start = [m.start() for m in re.finditer('<math',abc)]
end = [m.start() for m in re.finditer('</math',abc)]


startIn = []
endIn = []
i=0
counter=0
while(i < len(start)-1):
    startIn.append(start[i:i+len(RPAddress[counter])])
    endIn.append(end[i:i+len(RPAddress[counter])])
    i += len(RPAddress[counter])
    counter+=1
    
mathmlString = []

for i in range(0,len(RPAddress)):
    mathmlString.append([])
    
for i in range(0,len(startIn)):
    tempString=""""""
    for j in range(0,len(startIn[i])):
        mathmlString[i].append(abc[startIn[i][j]:endIn[i][j]+7].replace('\n','').replace('\t','').replace('  ',''))


mathmlString
PFs=[]
for i in range(0,len(mathmlString)):
    PFs.append([])
            
            
for i in range(0,len(mathmlString)):
    for j in range(0,len(mathmlString[i])):
        PFs[i].append(mathmlString[i][j][43+6:-7].replace("divide","div").replace("power","pow"))


PF=[]
for i in range(0,len(mathmlString)):
    PF.append([])
    
for i in range(0,len(PFs)):
    for j in range(0,len(PFs[i])):
        PF[i].append(mathmlToExp(PFs[i][j]))
PF


FinalPF = []
for i in range(0,len(mathmlString)):
    FinalPF.append([])

for i in range(0,len(PF)):
    for j in range(0,len(PF[i])):
        if(len(PFEnzyme[i][j])==0):
            FinalPF[i].append("pr = { " + PF[i][j] + " -> " + repartitionString[i][j] +" };")
        else:
            FinalPF[i].append("pr = { " + PF[i][j] +" [" + PFEnzyme[i][j][0] + "-> ] "+repartitionString[i][j] + " };")

fh = open('pepout.pep', 'w') 
fh.write('num_ps = {\n\n')
fh.write('H = {'+memString+"};\n\n")
fh.write('structure = '+structureF+';\n\n')
for i in range(0,len(memNames)):
    fh.write(memNames[i]+'='+'{\n'+varInitialValueString[i]+';\n'+enzymeString[i]+';\n'+("\n".join(string for string in FinalPF[i]))+"\n"+varInitialValues[i]+';\n'+enzymeInitialValueString[i]+';\n};\n\n')
fh.write('\n}')
fh.close()


