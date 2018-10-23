
# this program will open a .csv file, parse the attributes, and output an eagle script 
# that can be run in a schematic to update the attributes with the BOM data

import os, time, sys, re
import csv

defaultAttrs = ["Part", "Value", "Device", "Package", "Description"]
outputAttrs = ["MPN, MF, VOLTAGE, PACKAGE"]

class schematicItem:
    def __init__(self, refdes, attrDict):
        self.refdes = refdes
        self.attrDict = attrDict

    def output_scr(self):
        # This function will output a string that can be written as a line for an Eagle script
        outstr = ''
        for key in self.attrDict:
            if key not in defaultAttrs: # don't output the default attributes, or attributes with empty strings as values
                if self.attrDict[key]:
                    outstr += ("ATTR " + self.refdes + " " + str(key) + " \'" + self.attrDict[key] + "\';\n")
        return outstr

    def output_scr_mpn(self):
        # This function will output a string that can be written as a line for an Eagle script
        outstr = ''
        for key in self.attrDict:
            if key =='MPN' and self.attrDict[key]:
                outstr += ("ATTR " + self.refdes + " " + str(key) + " \'" + self.attrDict[key] + "\';\n")
        return outstr

currentpath = os.path.dirname(os.path.abspath(__file__))

# get file name from args, or try to find a bom in the current directory
file_path = ""
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    for fname in os.listdir(currentpath):
        if fname.endswith(".csv") and "bom" in fname.lower():
            file_path = fname;

print(file_path)

outputpath = currentpath + r'\eaglebomattr.scr'
output = open(outputpath, 'w')
headers = []
datalist = []
counter = 0
itemlist = []   # list of schematic Items

try:    
    firstline = True
    with open(file_path) as csvfile:
        for row in csv.reader(csvfile):
            if len(row) < 5:
                continue # skip line if less than 5 columns
            if firstline:
                headers = row
                firstline = False
                continue
            datadic = {}
            refdes = row[0]
        
            for i in range(1, len(row) - 1):
                datadic[headers[i]] = row[i]
        
            schitm = schematicItem(refdes, datadic)
            itemlist.append(schitm)

    print("Finished reading file")
    for item in itemlist:
        data = item.output_scr_mpn()
        output.write(data)

    output.write("GROUP ALL;\nCHANGE DISPLAY OFF (>0 0);")

except:
    print("Unable to open file")

output.close()
