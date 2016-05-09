'''
Created on May 8, 2016

@author: zhihuang
'''
from attacks.Attack import Attack
import math
import sys

class LogLikelihoodAttack(Attack):
    '''
    classdocs
    '''


    def __init__(self, refMAF = None, caseMAF = None):
        '''
        Constructor
        '''
        self.refMAF = refMAF
        self.caseMAF = caseMAF 
    
    def getAttackStatistic(self, victimSeq):
        L = 0
        for i in range(len(victimSeq)):
            refGenotypeFreqs = [(1 - self.refMAF[i]) * (1 - self.refMAF[i]),  # 0 minor allele
                                2 * (1 - self.refMAF[i]) * self.refMAF[i],  # 1 minor allele
                                self.refMAF[i] * self.refMAF[i]]  # 2 minor alleles
            caseGenotypeFreqs = [(1 - self.caseMAF[i]) * (1 - self.caseMAF[i]),
                                 2 * (1 - self.caseMAF[i]) * self.caseMAF[i],
                                 self.caseMAF[i] * self.caseMAF[i]]
            try:
                L += math.log(caseGenotypeFreqs[int(victimSeq[i])] / refGenotypeFreqs[int(victimSeq[i])])
            except:
                print i
                print caseGenotypeFreqs
                print refGenotypeFreqs
                sys.exit()
        return L
    
    def loadData(self, refMAFName, caseMAFName):
        refMAFFile = open(refMAFName)
        self.refMAF = [float(line.split()[1]) for line in refMAFFile]
        caseMAFFile = open(caseMAFName)
        self.caseMAF = [float(line.split()[1]) for line in caseMAFFile]
        
if __name__ == "__main__":
    attack = LogLikelihoodAttack()
#     attack.loadData("../../data/simulated/refMAF.txt", "../../data/simulated/caseMAF.txt")
    attack.loadData("../../data/simulated/refMAF.txt", "../../data/simulated/caseMAF_dp0.01.txt")
    case = open("../../data/simulated/case.txt")
    for i in range(5):
        victimSeq = [float(snp) for snp in case.readline().split()[1:]]
        stat = attack.getAttackStatistic(victimSeq)
        print stat
    test = open("../../data/simulated/test.txt")
    for i in range(5):
        victimSeq = [float(snp) for snp in test.readline().split()[1:]]
        stat = attack.getAttackStatistic(victimSeq)
        print stat