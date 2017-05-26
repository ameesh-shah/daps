import yaml
import numpy as np
import sys

'''
HOW TO USE:
This program, the second part of the data generation pipeline, will take in a modified YAML file,
that the user has entered probability distributions for, and will generate random data based on those
grammar rules and probabilities.

USAGE: First, go to the YAML file produced by createYAMLFromYacc.py and MAKE SURE that you have
filled the spaces where probabilities should go. These should all be numbers less than or equal
to 1! If your probabilties are wrong or unfilled, this program will break down.
Like the previous program, the command line usage will take two arguments. The first will take in
the modified YAML file, and the second will be the number of symbols that you want to produce
from the pseudo-random data generation. The third will be the out file for the text that will be
produced. Example:

python generateDataFromYAML.py "myModifiedYAML.yaml" 10000 "textfile.txt"

Best of luck!

author ameeshshah
'''

class Rule:
    def __init__(self, name):
        self.lhs = name
        self.rhs = []
        self.rhsProbs = []
        self.numRHS = 0

    def add_rhs(self, expression1):
        self.rhs.append(expression1)
        self.numRHS = self.numRHS + 1

    def print_rules(self):
        for singleRHS in self.rhs:
            print singleRHS.expansion


class CFG:
    def __init__(self):
        self.tokens = {}
        self.rules = []
        self.lhs = {}
        self.numLHS = 0
        self.numtokens = 0

        # BELOW are fields used only to save computations
        # when generating random samples.
        self.lhsToSample = []
        self.lhsProbsToSample = []



    def add_tokens(self, tokendict):
        for token in tokendict:
            # adds tokens
            # myCFG.add_token(token)
            realizationProb = {}
            for realization in tokendict[token]:
                # adds realizations and realization probabilities in realizations field
                realizationProb[realization] = tokendict[token][realization]
            self.tokens[token] = realizationProb
            self.numtokens += 1

    def add_rule(self, rule):
        self.rules.append(rule)
        self.numLHS = self.numLHS + 1

    def setup_Tokens(self):
        self.numtokens = len(self.tokens)

    def printz(self):
        for rule in self.rules:
            print '\n\n Name of the rule is : ', rule.lhs, '\n'
            for singleRHS in rule.rhs:
                print singleRHS


    def num_rhs(self, lhsName):
        return len(self.rules[self.which_lhs(lhsName)].rhs)

    def num_rhs_terms(self, lhsName, rhsNum):
        return len(self.rules[self.which_lhs(lhsName)].rhs[rhsNum])

    def sample_token(self, tokenName):
        '''
        :param tokenName: the name of a token in the token field
        :return: a psuedo-random realization of the token based on the probability distribution
        of those realizations.
        '''
        realizations = []
        realizationProbs = []
        realDict = self.tokens[tokenName]
        for realization in realDict:
            realizations.append(realization)
            realizationProbs.append(realDict[realization])
        choice = np.random.choice(realizations, 1, p=realizationProbs)
        return choice[0]

    def sample_RHS(self, lhsName):
        '''
        :param lhsName: the name of the LHS from which we sample an RHS
        :return: an RHS based on the probability distributions indicated in the rule
        '''
        for rule in self.rules:
            if rule.lhs == lhsName:
                sampledRHS = np.random.choice(rule.rhs, 1, p=rule.rhsProbs)
                break
        return sampledRHS[0]

    def is_token(self, thing):
        return thing.isupper()

    def sample_LHS(self):
        '''
        :return: a random lhs based on the probability distributions
        '''
        choice = np.random.choice(self.lhsToSample, 1, p=self.lhsProbsToSample)
        return choice[0]

    def gen_from_start_lhs(self, lhsName):
        sampledRHS = list(self.sample_RHS(lhsName))
        sentence = []
        while sampledRHS:
            if self.is_token(sampledRHS[0]):
                sampledToken = self.sample_token(sampledRHS[0])
                sentence += sampledToken.__str__()
                sampledRHS.remove(sampledRHS[0])
            elif sampledRHS[0] in self.lhs:
                temptemp = []
                temptemp = list(self.sample_RHS(sampledRHS[0]))
                sampledRHS.remove(sampledRHS[0])
                sampledRHS = temptemp + sampledRHS
            else:
                sentence += sampledRHS[0].__str__()
                sampledRHS.remove(sampledRHS[0])
        sentence = "".join(sentence)
        return sentence

    def gen_min_symbols(self, minSymbols):
        lhsName = self.sample_LHS()
        sentence = self.gen_from_start_lhs(lhsName)
        while len(sentence) < minSymbols:
            tempSent = self.gen_from_start_lhs(lhsName)
            sentence = sentence + tempSent
        return sentence

    def gen_transition_mat(self):
        stuff = 1

        return stuff

def read_yaml_file(yamlfile):
    with open(yamlfile, 'r') as stream:
        try:
            yamldict = yaml.safe_load(stream)
            return yamldict
        except yaml.YAMLError as exc:
            print("EXC" + exc.__str__())


def createCFG(masterdict):
    myCFG = CFG()
    tokendict = masterdict['Tokens']
    # adds tokens, their realizations, and those probabilities
    myCFG.add_tokens(tokendict)

    myCFG.setup_Tokens()

    lhsdict = masterdict['LHS']
    for lhs in lhsdict:
        myCFG.numLHS += 1
        myCFG.lhs[lhs] = lhsdict[lhs]['LHS PROBABILITY:']
        productionrules = lhsdict[lhs]
        addrule = Rule(lhs)
        for rule in productionrules:
             if rule != 'LHS PROBABILITY:':
                if rule != 'empty':
                    newrule  = rule.split(' ')
                    #print rule
                    addrule.rhs.append(newrule)
                    addrule.rhsProbs.append(productionrules[rule])
                else:
                    newrule = []
                    addrule.rhs.append(newrule)
                    addrule.rhsProbs.append(productionrules[rule])
                addrule.numRHS += 1
             else:
                continue
        myCFG.add_rule(addrule)

    for single in myCFG.lhs:
        myCFG.lhsToSample.append(single)
        myCFG.lhsProbsToSample.append(myCFG.lhs[single])

    return myCFG


masterdict = read_yaml_file("languageraw.yaml")
myCFG = createCFG(masterdict)
sentence = myCFG.gen_min_symbols(1000)
text_file = open("mathStackD2Testing.txt", "w")
text_file.write(sentence.replace('\\n', '\n'))
text_file.close()

# if __name__ == "__main__":
#     #get arguments from command line
#     arguments = sys.argv
#     yamlfile = arguments[1]
#     numsymbols = arguments[2]
#     textFileName = arguments[3] #"cLanguageGen.txt"
#
# 	#myCFG.printz()
#
#     #create dictionary from yaml which will fill up the CFG
#     masterdict = read_yaml_file(yamlfile)
#     #create the CFG with tokens, LHS and RHS rules from dictionary
#     myCFG = createCFG(masterdict)
#     # generate the min symbols by sampling from the probability distributions
#     sentence = myCFG.gen_min_symbols(numsymbols)
#     text_file = open(textFileName, "w")
#     text_file.write(sentence.replace('\\n', '\n'))
#     text_file.close()
