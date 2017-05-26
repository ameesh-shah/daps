'''
FileName: ProcessStackOutput.py
Author: Rice DSP (Joshua Michalenko)
Date: 03/20/2017
Purpose: This script works in tandem with the "makeStates.sh" script. It takes the output
         of the script which is some debugging infromation with some token lengths 
         appended to it and it first creates a data structure of how long each of the 
         parsed tokens is (+1 for the whitespace char). The Script then parses up the 
         debugging information from the bison parser to grab the stack state at each 
         token encountered during parsing. The script then writes the stack state to
         a csvFile zero padded to a length according to the variable MAXSTACK. Each Stack
         state is repeated for the number of characters of each token (+1 for whitespace
         if there is whitespace). 

Use case: python processStackOutput.py <Output CSV File>.csv

Arguments: arg1 - <Output CSV File>.csv - (OUTPUT) - A outputted csv file of the proccessed 
                stack states.

Input Files: stackStates.out - A simple output file produced from "makeStates.sh"

Output Files: processedStates.csv - CSV with the number of rows equal to the number of 
                        characters in the input file. The first column will be the 
                        token read by the parser, the rest of the columns are the 
                        stack states at each chararacter. 
'''


import numpy as np
import re
import os
import string
import sys

argumentList = sys.argv

outCSVFile = argumentList[1] #"processedStackStates.csv"

# name of input and a temp output file
inputFilename = 'stackStates.out'
outputFilename = 'stackStates.txt'
## consolidate the list for whitespaces
#give max stack depth to zero pad accordingly
MAXSTACK = 30

#read in the outfile from 'makeStates'
fh = open(inputFilename, 'r')
#Cheap way to get the last line
for line in fh:
        iterators = line

#instead of seperating by commas, seperate by newlines.
iterators = iterators.replace(',',"\n")
whitespace = 0
clockTick = []
cnt = 0
whitespaceFlag = 0

#Count up the lengths of each of the tokens, tack on white space length
#So that we have a vector of integers which are the lengths of each token
# plus the subsequent whitespace.
# As a sanity check, the sum of the vector should be number of characters
# in the input file. 
for line in iterators.splitlines():
        if line.startswith('w'):
                line = line.replace('w','')
                whitespace = int(line)
                whitespaceFlag = 1

        if whitespaceFlag == 1:  
                clockTick[cnt-1] = clockTick[cnt-1] + whitespace             
                whitespaceFlag = 0
        else:
                clockTick.insert(cnt,int(line))
                cnt=cnt+1

clockTick = np.array(clockTick)
#end of consolidation
#create processed csv file


fIn = open(inputFilename, 'r')
fOut = open(outputFilename, 'w')

currentStackNow = ''
nextTokenReached = 0
allStackStates = ''
ticker = 0
lastHitShift = 0

numTicks = len(clockTick)

#Stupid way to do it but basically this for look write the stack info plus the number
#of times to repeat it to a temp file
for line in fIn:
        if line.startswith('Shifting token') and ticker < numTicks:
                tempLine = re.match("\Shifting token (.*) \(",line)
                fOut.write(currentStackNow)

                fOut.write(tempLine.group(1)+ ' ' + str(clockTick[ticker])+"\n")
                ticker = ticker + 1

        if line.startswith('Stack now'):
                currentStackNow = line

fOut.write('Stack now 0')

fOut.close()
fIn.close()

inputFilename = 'stackStates.txt'
outputFilename = outCSVFile 

fIn = open(inputFilename, 'r')
fOut = open(outputFilename, 'w')
cnt = 0
ticker = 0

#Read in the temp file and repeat the stack state the number of characters in the 
#corresponding token, Also zero pad

for line in fIn:
        if cnt % 2 == 0:
                part1 = line
                cnt = cnt+1
        else:
                for ii in xrange(clockTick[ticker]):
#                        tempString =  part1.strip() + line.strip()
#                        # tempString = 'comment 34Stack now 4 2 454'
#                        #stringWOStacknow = re.sub('[0-9]+Stack now ' , '', tempString)
#                        stringWOStacknow = re.sub('Stack now ', '' , tempString)                        
#                        writeOutString = re.subn(' ',',',stringWOStacknow)
#                        fOut.write(writeOutString[0])
#                        
#                        # zero pad the rest
                        aa = re.search('([^\s]+)',line)
                        fOut.write(aa.group(0))
                        stringWOStackNow = re.search('Stack now(.*)',part1.strip())
                        tempString = re.subn(' ', ',',stringWOStackNow.group(1))
                        fOut.write(tempString[0])
                        for jj in xrange(MAXSTACK-tempString[1]):
                             fOut.write(',0')

                        fOut.write("\n")

                ticker = ticker +1
                cnt = cnt+1

fOut.close()
fIn.close()










