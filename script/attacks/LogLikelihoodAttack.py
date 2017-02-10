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
    
    def getAttackStatistic(self, numOfSNPs, victimSeq):
        L = 0
        for i in range(numOfSNPs):
            refGenotypeFreqs = [(1 - self.refMAF[i]) * (1 - self.refMAF[i]),  # 0 minor allele
                                2 * (1 - self.refMAF[i]) * self.refMAF[i],  # 1 minor allele
                                self.refMAF[i] * self.refMAF[i]]  # 2 minor alleles
            caseGenotypeFreqs = [(1 - self.caseMAF[i]) * (1 - self.caseMAF[i]),
                                 2 * (1 - self.caseMAF[i]) * self.caseMAF[i],
                                 self.caseMAF[i] * self.caseMAF[i]]
            
            L += math.log(caseGenotypeFreqs[int(victimSeq[i])] / (refGenotypeFreqs[int(victimSeq[i])] + 1e-80) + 1e-80)
        return L
    
    def loadData(self, refMAFName, caseMAFName):
        refMAFFile = open(refMAFName)
        self.refMAF = [float(line.split()[1]) for line in refMAFFile]
        caseMAFFile = open(caseMAFName)
        self.caseMAF = [float(line.split()[1]) for line in caseMAFFile]
        
def performAttack(numOfVictims, numOfSNPs, sanitizationSuffix):
    attack = LogLikelihoodAttack()
    attack.loadData("../../data/simulated/refMAF.txt", "../../data/simulated/caseMAF_" + sanitizationSuffix + ".txt")
    case = open("../../data/simulated/case.txt")
    caseStats = []
    for i in range(numOfVictims):
        victimSeq = [float(snp) for snp in case.readline().split()[1:]]
        stat = attack.getAttackStatistic(numOfSNPs, victimSeq)
        caseStats.append(stat)
    test = open("../../data/simulated/test.txt")
    testStats = []
    for i in range(numOfVictims):
        victimSeq = [float(snp) for snp in test.readline().split()[1:]]
        stat = attack.getAttackStatistic(numOfSNPs, victimSeq)
        testStats.append(stat)
    
    file = open("../../data/simulated/attackStats/LLR_caseAttackStats_" + sanitizationSuffix + "_" +  str(numOfSNPs) + "SNPs.txt", 'w')
    file.write('\n'.join([str(x) for x in caseStats]))
    file.close()
    file = open("../../data/simulated/attackStats/LLR_testAttackStats_" + sanitizationSuffix + "_" +  str(numOfSNPs) + "SNPs.txt", 'w')
    file.write('\n'.join([str(x) for x in testStats]))
    file.close()


if __name__ == "__main__":
    # For cluster
    import sys
    arg = sys.argv
    performAttack(1000, int(arg[1]), arg[2])
    # End for cluster
    #performAttack(3, 10, "dp0.1")