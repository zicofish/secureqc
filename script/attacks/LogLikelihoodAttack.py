'''
Created on May 8, 2016

@author: zhihuang
'''
from attacks.Attack import Attack
import math
from scipy.stats import norm

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
    
def LStats2PValues(poolSize, numOfSNPs, sanitizationSuffix, group):
    statFile = open("../../data/simulated/attackStats/LLR_" + group + "AttackStats_" + sanitizationSuffix + "_" + str(numOfSNPs) + "SNPs.txt")
    pvalueFile = open("../../data/simulated/attackStats/LLR_" + group + "PValues_" + sanitizationSuffix + "_" + str(numOfSNPs) + "SNPs.txt", 'w')
    pValues = []
    gaussian = norm(loc = -numOfSNPs / (2*poolSize), scale = math.sqrt(numOfSNPs / poolSize))
    for line in statFile.readlines():
        pValues.append(gaussian.sf(float(line)))
    pvalueFile.write('\n'.join([str(x) for x in pValues]))
    pvalueFile.close()
    

if __name__ == "__main__":
    # For cluster
#     import sys
#     arg = sys.argv
#     performAttack(1000, int(arg[1]), arg[2])
    # End for cluster
    #performAttack(3, 10, "dp0.1")
    numOfSNPsList = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    saniList = ["clear", "dp0.1_delta0.01", "dp0.1_delta0.05", "dp0.1_delta0.001", "dp0.1_delta0.005",
                "dp0.05_delta0.01", "dp0.05_delta0.001", "dp0.05_delta0.05", "dp0.05_delta0.005"]
    groupList = ['case', 'test']
    for numOfSNPs in numOfSNPsList:
        for sani in saniList:
            for group in groupList:
                LStats2PValues(1000, numOfSNPs, sani, group)