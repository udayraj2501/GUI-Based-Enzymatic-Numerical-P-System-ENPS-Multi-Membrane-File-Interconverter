import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]


import numpy as np
import xml.etree.ElementTree as ET

file = open(arguments[0], 'r')

f=0
while(f==0):
    line=file.readline()
    for i in range(0,len(line)):
        if(line[i]=='#'):
            line=line[0:i].strip()
            break
    for i in range(0,len(line)):
        if(line[i]=='H'):
            for j in range(i,len(line)):
                if(line[j]==';'):
                    membranesList=line[i:j+1].strip()
                    break
            f=1
            break

for i in range(0,len(membranesList)):
    if(membranesList[i]=='{'):
        membranesList=membranesList[i+1:].strip()
        break
membranesList=membranesList[:-2].split(',')
x2=[]
x2.append(membranesList)
x2.append(([i for i in range(0,len(membranesList))]))
x2=np.transpose(x2)
membraneList={k.strip():v.strip() for (k,v) in x2}      # to make a dictionary of membrane names

file.seek(0)
f=0
ln=0
pos=-1
while(f==0):
    line=file.readline()
    ln+=1
    for i in range(0,len(line)):
        if(line[i]=='#'):
            line=line[0:i].strip()
            break
    for i in range(0,len(line)):
        if(line[i:i+9]=='structure'):
            for j in range(i,len(line)):
                if(line[j]==';'):
                    x2=line[i:j+1].strip()
                    pos=j+1
            f=1
            break
x2=x2[12:]

stack=[]
block=[]
memCount=0
semicoloncount=0
for i in range(0,len(membraneList)):
    block.append("")
file.seek(0)
while(memCount<len(membraneList)):
    x=file.readline()
    for i in range(0,len(x)):
        if(x[i]==';'):
            semicoloncount+=1
        if(semicoloncount>=2):
            block[memCount]+=x[i]
            if(x[i]=='{'):
                stack.append('{')
            elif(x[i]=='}'):
                stack.pop()
                if(len(stack)==0):
                    memCount+=1
                    if(memCount==len(membraneList)):
                        break

y=[]
for i in range(0,len(block)):
    x=block[i].split('\n')
    for i in range(0,len(x)):
        for j in range(0, len(x[i])):
            if(x[i][j]=='#'):
                x[i]=x[i][0:j].strip()
                break
        if(x[i].strip()):
            x[i]=x[i].strip()
    y.append(x)

newS=[]
for i in range(0,len(y)):
    newS.append("")
for i in range(0,len(y)):
    for j in range(0,len(y[i])):
        newS[i]=newS[i]+(y[i][j])
m=[]
for i in range(0,len(newS)):
    m.append(newS[i].split(';'))

for i in range(0,len(m)):
    MM=""
    VL=""
    x=m[i][0]
    MM=x[0:x.find('=')]
    VL=x[x.find('{')+1:]
    del m[i][0]
    m[i].insert(0,VL.strip())
    m[i].insert(0,MM.strip())
y=m

maxRules=0
for i in range(0, len(y)):
    localMaxRules=0
    for j in range(0, len(y[i])):
        if('pr' in y[i][j]):
            localMaxRules+=1
        if(localMaxRules>maxRules):
            maxRules=localMaxRules
maxRules+=1

aot = [[[[0 for l in range(5)] for k in range(maxRules)] for j in range(5)] for i in range(len(membraneList))]

Maintree=ET.Element('membraneSystem',{'type':'ENPS','xmlns':'http://www.example.org'})
stack=[]
firstStr=""
for i in range(1,len(x2)):
    if(x2[i]=='[' or x2[i]==']'):
        m=i
        break
    firstStr+=x2[i]
stack.append(firstStr.strip())

aot[(int)(membraneList[firstStr.strip()])][0][0][0]=ET.SubElement(Maintree,'membrane',{'name':firstStr.strip()})
aot[(int)(membraneList[firstStr.strip()])][1][0][0]=ET.SubElement(aot[(int)(membraneList[firstStr.strip()])][0][0][0],'region')
aot[(int)(membraneList[firstStr.strip()])][2][0][0]=ET.SubElement(aot[(int)(membraneList[firstStr.strip()])][1][0][0],'memory')
aot[(int)(membraneList[firstStr.strip()])][3][0][0]=ET.SubElement(aot[(int)(membraneList[firstStr.strip()])][1][0][0],'rulesList')
aot[(int)(membraneList[firstStr.strip()])][4][0][0]=ET.SubElement(aot[(int)(membraneList[firstStr.strip()])][0][0][0],'children')

string=""
for i in range(m+1,len(x2)):
    if(x2[i]==';'):
        break;
    if(x2[i]=='[' or x2[i]==']'):
        if(stack[-1]!=string.strip()):
            aot[(int)(membraneList[string.strip()])][0][0][0]=ET.SubElement(aot[(int)(membraneList[stack[-1].strip()])][4][0][0],'membrane',{'name':string.strip()})
            aot[(int)(membraneList[string.strip()])][1][0][0]=ET.SubElement(aot[(int)(membraneList[string.strip()])][0][0][0],'region')
            aot[(int)(membraneList[string.strip()])][2][0][0]=ET.SubElement(aot[(int)(membraneList[string.strip()])][1][0][0],'memory')
            aot[(int)(membraneList[string.strip()])][3][0][0]=ET.SubElement(aot[(int)(membraneList[string.strip()])][1][0][0],'rulesList')
            aot[(int)(membraneList[string.strip()])][4][0][0]=ET.SubElement(aot[(int)(membraneList[string.strip()])][0][0][0],'children')
            stack.append(string.strip())
        else:
            stack.pop()
        string=""
    else:
        string+=x2[i]

prIndex=[]
for i in range(0,len(membraneList)):
    prIndex.append([])
    
for i in range(0,len(y)):
    for j in range(0,len(y[i])):
        if( "pr" in y[i][j]):
            prIndex[i].append(j)

for i in range(0,len(prIndex)):
    for j in range(0,len(prIndex[i])):
            aot[i][3][j+1][0] = ET.SubElement(aot[i][3][0][0],'rule')
            aot[i][3][j+1][1] = ET.SubElement(aot[i][3][j+1][0],'repartitionProtocol')
            aot[i][3][j+1][2] = ET.SubElement(aot[i][3][j+1][0],'productionFunction')
            aot[i][3][j+1][3] = ET.SubElement(aot[i][3][j+1][2],'math',{'xmlns':"http://www.w3.org/1998/Math/MathML"})

varValList=[]
vtemp=""
index = []

for i in range(0,len(y)):
    vtemp=""
    for j in range(0,len(y[i])):         #Getting the Initailvalues of the variables and storing them in a
        if("var0" in y[i][j]):                #2D array(var1) for future reference.                 
            index.append(j)

for i in range(0,len(index)):
    vtemp=""
    for j in range(0,len(y[i][index[i]])):
        
        if(y[i][index[i]][j] == "("):
                k=j+1
                while(y[i][index[i]][k] != ")"):
                    vtemp+=y[i][index[i]][k]
                    k+=1
                varValList.append(vtemp.split(","))

varIndex=[]
for i in range(0,len(y)):
    vtemp=""
    for j in range(0,len(y[i])):
        if('var ' in y[i][j]):
#         if(y[i][j][:4]=="var "):
            varIndex.append(j)


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

varList=[]
vtemp=""
for i in range(0,len(varIndex)):
    vtemp=""
    for j in range(0,len(y[i][varIndex[i]])):            
        secondIndex = find_nth(y[i][varIndex[i]],'{',2)
        if(j == secondIndex):                              #2D array(var) for future reference.
            k=j+1
            while(y[i][varIndex[i]][k]!="}"):
                vtemp+=y[i][varIndex[i]][k]
                k+=1   
            varList.append(vtemp.split(","))


for i in range(0,len(varList)):
    for j in range(0,len(varList[i])):
#         print(i,j)
        aot[i][2][1][0]=ET.SubElement(aot[i][2][0][0],'variable',{'initialValue':varValList[i][j].strip(),'input':'true','output':'true'})
        aot[i][2][1][0].text = varList[i][j].strip()

RV=[]
for i in range(0,len(prIndex)):
    RV.append([])
    for j in range(0,len(prIndex[i])):
        RV[i].append([])
vtemp=""
for i in range(0,len(prIndex)):
    for j in range(0,len(prIndex[i])):
        for l in range(0,len(y[i][prIndex[i][j]])):
            if(y[i][prIndex[i][j]][l] == "|"):
                k=l-1
                while(y[i][prIndex[i][j]][k].isdigit()):
                        vtemp+=y[i][prIndex[i][j]][k]
                        k-=1
                RV[i][j].append(ET.SubElement(aot[i][3][j+1][1],'repartitionVariable',{'contribution':vtemp[::-1].strip()}))
                vtemp=""

RVNames=[]
for i in range(0,len(prIndex)):
    RVNames.append([])
    for j in range(0,len(prIndex[i])):
        RVNames[i].append([])

vtemp=""
for i in range(0,len(prIndex)):
    for j in range(0,len(prIndex[i])):
#         print(i,j)
        for l in range(0,len(y[i][prIndex[i][j]])):
            if(y[i][prIndex[i][j]][l] == "|"):
                k=l+1
                while(y[i][prIndex[i][j]][k].isdigit() or y[i][prIndex[i][j]][k] == '_' or y[i][prIndex[i][j]][k].isalpha()):
                    vtemp+=y[i][prIndex[i][j]][k]
                    k+=1
                
                RVNames[i][j].append(vtemp)
                vtemp=""

for i in range(0,len(RVNames)):
    for j in range(0,len(RVNames[i])):
        for k in range(0,len(RVNames[i][j])):
            RV[i][j][k].text = RVNames[i][j][k]

from sympy import *

string=''
stemp=[]
for i in range(0,len(y)):
    stemp.append([])
for i in range(0,len(y)):
    for j in range(0,len(y[i])):
        if("pr" in y[i][j]):
            for k in range(0,len(y[i][j])):
                if(y[i][j][k] == '{'):
                    o=k+1
                    while(y[i][j][o] != "[" and y[i][j][o] != '>'):
                        string+=y[i][j][o]
                        o+=1
                    string = string[:]
                    stemp[i].append(string.replace(" ",""))
#                     print(string)
                    string = "" 

noOfVariables = []
for i in range(0,len(stemp)):
    noOfVariables.append([])
for i in range(0,len(stemp)):
    for j in range(0,len(stemp[i])):
        counter=0
        for k in range(0,len(stemp[i][j])):
            if(stemp[i][j][k] == "/" or stemp[i][j][k] == "*" or stemp[i][j][k] == "-" or stemp[i][j][k] == "+" or stemp[i][j][k] == "^"):
                counter+=1
        noOfVariables[i].append(counter+1)


enzyme = []
# for i in range(0,len(membraneList)):
#     enzyme.append([])
for i in range(0,len(y)):
    flag=0
    for j in range(0,len(y[i])):
        if(y[i][j][:2] == "E0"):
            flag=1
            for k in range(0,len(y[i][j])):
                if(y[i][j][k] == '('):
                    o=k+1
                    while(y[i][j][o] != ')'):
                        string+=y[i][j][o]
                        o+=1
                    
                    enzyme.append(string.split(","))
                    string=""
    if(flag == 0):
        enzyme.append([])

EnzymeName = []
for i in range(0,len(prIndex)):
    EnzymeName.append([])
    
string=''
for i in range(0,len(prIndex)):
    for j in range(0,len(prIndex[i])):
        for l in range(0,len(y[i][prIndex[i][j]])):
            len_pr = len(y[i][prIndex[i][j]])
            if( (l < len_pr) and (y[i][prIndex[i][j]][l] == '[')):
                len_ab = len(y[i][prIndex[i][j]])
                k=l+1
                while( (k < len_ab) and ( y[i][prIndex[i][j]][k] == '_' or y[i][prIndex[i][j]][k].isdigit() or y[i][prIndex[i][j]][k].isalpha() or y[i][prIndex[i][j]][k] == " " ) ) :
                    string+=y[i][prIndex[i][j]][k]
                    k+=1
        
                EnzymeName[i].append(string.strip())
                string=''

EnzymeNameList=[]
    
for i in range(0,len(y)):
    flag=0
    for j in range(0,len(y[i])):
        if(y[i][j][:1] == "E"):
            flag=1
            for k in range(0,len(y[i][j])):
                if(y[i][j][k] == '{'):
                    o=k+1
                    while(y[i][j][o] != '}'):
                        string+=y[i][j][o]
                        o+=1
                    
                    EnzymeNameList.append(string.split(","))
                    string=""
    if(flag == 0):
        EnzymeNameList.append([])

for i in range(0,len(enzyme)):
    for j in range(0,len(enzyme[i])):
        aot[i][2][1][0] = ET.SubElement(aot[i][2][0][0],'variable',{'initialValue':enzyme[i][j].strip(),'stop':'true'})
        aot[i][2][1][0].text = EnzymeNameList[i][j].strip()

dicti=[]
for i in range(0,len(prIndex)):
    dicti.append([])
    for j in range(0,len(prIndex[i])):
        dicti[i].append([])

replacement=[]

for i in range(65,91):
    replacement.append(chr(i))
for i in range(65,91):
    replacement.append(chr(65)+chr(i))
for i in range(65,91):
    replacement.append(chr(66)+chr(i))
for i in range(65,91):
    replacement.append(chr(67)+chr(i))

strings = stemp

variableToBeReplaced=''
whileLoopincrement=0
for i in range(0,len(strings)):
    for j in range(0,len(strings[i])):
        count=0
        l=0
        lenOfEachString=len(strings[i][j])
        while(l < lenOfEachString):
            
            newLength = len(strings[i][j])
#             print('l'+str(l))
#             print(strings[i][j])
            if( (l < newLength) and (strings[i][j][l].isalpha()) ):
#                 print('if'+str(i),str(j))
                k = l 
                while( (k < newLength) and (strings[i][j][k].isalpha() or strings[i][j][k] == '_' or strings[i][j][k].isdigit() )   ):
#                     print('k'+str(k))
                    variableToBeReplaced+=strings[i][j][k]
                    k+=1                
                variableToBeReplaced.strip()
#                 print(variableToBeReplaced)
#                 print('!'+str(l)+'!'+str(k))
                dicti[i][j].append(variableToBeReplaced)
                strings[i][j] = strings[i][j].replace("^","**")
                strings[i][j] = strings[i][j].replace(variableToBeReplaced,str(replacement[count]),1)
                count+=1
                variableToBeReplaced=''
                l+= 1
            else:
#                 print('else'+str(i),str(j))
                l+=1

stemp = strings

UU = Symbol("UU")

A = Symbol("A")
B = Symbol("B")
C = Symbol("C")
D = Symbol("D")
E = Symbol("E")
F = Symbol("F")
G = Symbol("G")
H = Symbol("H")
I = Symbol("I")
J = Symbol("J")
K = Symbol("K")
L = Symbol("L")
M = Symbol("M")
N = Symbol("N")
Y = Symbol("O")
P = Symbol("P")
Q = Symbol("Q")
R = Symbol("R")
S = Symbol("S")
T = Symbol("T")
U = Symbol("U")
V = Symbol("V")
W = Symbol("W")
X = Symbol("X")
Y = Symbol("Y")
Z = Symbol("Z")
AA = Symbol("AA")
AB = Symbol("AB")
AC = Symbol("AC")
AD = Symbol("AD")
AE = Symbol("AE")
AF = Symbol("AF")
AG = Symbol("AG")
AH = Symbol("AH")
AI = Symbol("AI")
AJ = Symbol("AJ")
AK = Symbol("AK")
AL = Symbol("AL")
AM = Symbol("AM")
AN = Symbol("AN")
AO = Symbol("AO")
AP = Symbol("AP")
AQ = Symbol("AQ")
AR = Symbol("AR")
AS = Symbol("AS")
AT = Symbol("AT")
AU = Symbol("AU")
AV = Symbol("AV")
AW = Symbol("AW")
AX = Symbol("AX")
AY = Symbol("AY")
AZ = Symbol("AZ")

BA = Symbol("BA")
BB = Symbol("BB")
BC = Symbol("BC")
BD = Symbol("BD")
BE = Symbol("BE")
BF = Symbol("BF")
BG = Symbol("BG")
BH = Symbol("BH")
BI = Symbol("BI")
BJ = Symbol("BJ")
BK = Symbol("BK")
BL = Symbol("BL")
BM = Symbol("BM")
BN = Symbol("BN")
BO = Symbol("BO")
BP = Symbol("BP")
BQ = Symbol("BQ")
BR = Symbol("BR")
BS = Symbol("BS")
BT = Symbol("BT")
BU = Symbol("BU")
BV = Symbol("BV")
BW = Symbol("BW")
BX = Symbol("BX")
BY = Symbol("BY")
BZ = Symbol("BZ")
CA = Symbol("CA")
CB = Symbol("CB")
CC = Symbol("CC")
CD = Symbol("CD")
CE = Symbol("CE")
CF = Symbol("CF")
CG = Symbol("CG")
CH = Symbol("CH")
CI = Symbol("CI")
CJ = Symbol("CJ")
CK = Symbol("CK")
CL = Symbol("CL")
CM = Symbol("CM")
CN = Symbol("CN")
CO = Symbol("CO")
CP = Symbol("CP")
CQ = Symbol("CQ")
CR = Symbol("CR")
CS = Symbol("CS")
CT = Symbol("CT")
CU = Symbol("CU")
CV = Symbol("CV")
CW = Symbol("CW")
CX = Symbol("CX")
CY = Symbol("CY")
CZ = Symbol("CZ")

abc=[]
for i in range(0,len(stemp)):
    for j in range(0,len(stemp[i])):
        for l in range(0,len(stemp[i][j])):
            s = mathml(eval(stemp[i][j]))
#             print(s)
            for m in range(0,len(dicti[i][j])):
                s = s.replace(str(replacement[m]),dicti[i][j][m])
                s = s.replace('power','pow').replace('divide','div').replace('plus','add')
#             print(s)
            k = ET.XML(s)
#             print(k)
        aot[i][3][j+1][3].append(k)



for i in range(0,len(EnzymeName)):
    count=1
    for j in range(0,len(EnzymeName[i])):
        aot[i][3][count][4] = ET.SubElement(aot[i][3][count][0],'enzyme')
        aot[i][3][count][4].text = EnzymeName[i][j]
        count+=1


xml = ET.ElementTree(Maintree)
xml.write("xmlout.xml")


