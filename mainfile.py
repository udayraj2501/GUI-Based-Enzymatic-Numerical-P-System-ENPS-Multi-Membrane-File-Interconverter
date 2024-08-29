import os


print('Multi-Membrane and Multi-siumulator Support tool')
print('1. Converting from PeP to XML')
print('2. Converting from XML to PeP')
print('3. Multiple Membrane Execution in PeP')
print('4. Multiple Membrane Execution in XML')
choice = input('Make a Choice')


if(choice=='1'):
	filename = input ('Enter the PeP file name for conversion')
	os.system('python3 peptoxml.py ' + filename)
if(choice=='2'):
	filename = input ('Enter the XML file name for conversion')
	os.system('python3 xmltopep.py ' + filename)			
if(choice=='3'):
	os.system('python3 transferValuesPep.py')
if(choice=='4'):
	os.system('python3 transferValuesXml.py')
