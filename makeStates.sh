#!/bin/bash

#File - makeStates.sh
#Date - 04/06/2017
#Author - Rice DSP (Joshua Michalenko, ameeshshah)
#Purpose - The purpose of the bash script is to run the stack generation process. given a lex, yacc, and text file, 
#	   The stack generator will create a parser, then use that parser to produce some debugging information
#	   The degugging information has the stack states in it, so the processStackOutput.py Script parses and 
#	   formates the log file to produce and .csv file of the processed Stack States.
#
# Use Case: "./makeStates.sh <yacc File> <Desired Directory> <Lex File> <Text File> <Ouput csvFile>"
#	    
#
# Arguments - arg1 -  <yacc File>  - (INPUT) the input .y yacc file with the language specification, typically
#			has the form <name>.y
#
# 	      arg2 - <Lex File> - (INPUT) the name of the .l lex file with the language specification. Be sure this
#			file has the correct form specified in the README. Typically has the form <name>.l
#
#	      arg3 - <Text File> - (INPUT) The name of the arbitrary text file that follows the yacc/lex specification
#			that the stack states will be produced for. This file can have any form as long as it abides by
#			the language specification.
#
#	      arg4 - <Ouput csvFile> - (OUTPUT) The name of the csv file that will be outputted for the program.
#			Typically has the form <name>.csv
#
# 
# Note: $1 - ABHeiracyLang.y
#	$2 - ABHeiracyLang.l
#	$3 - ABOutput100.txt
#	$4 - processedStackStates.csv 	
# Quick Test: ./makeStates.sh ABHeiracyLang.y ABHeiracyLang.tab.c ABHeiracyLang.l ABOutput100.txt processedStackStates1.csv

#set for error handling to output if something goes wrong and bash throws an exception.
set -e

#create tokenizer lex.yy.c
lex $2 

#create parser with some debugging properties
bison -dtv $1 -b currentLang


#compile the tokenizer and parser together in one package
cc lex.yy.c currentLang.tab.c -o stackViewer

#extract the token lengths, then extract debugging output to scrape
./stackViewer< $3 > charLeng.out
./stackViewer< $3 2> debugOutput.out
cat debugOutput.out charLeng.out > stackStates.out

#scrape the debugging information and output a .csv file with stack states
python processStackOutput.py $4

#move parser files to correct directory
rm currentLang.tab.c 
rm currentLang.tab.h 
rm currentLang.output 

#clean up directory of all those pesky temp files
rm stackStates.out
rm debugOutput.out
rm charLeng.out
rm stackViewer
rm lex.yy.c
rm stackStates.txt

#print out that you finished
echo \n
echo Wowzas!!!!
echo Ignore all of the junk that just got printed.
echo Stack states have been generated successfully!
