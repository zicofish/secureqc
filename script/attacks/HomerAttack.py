'''
Created on May 2, 2016

@author: zhihuang
'''
from attacks.Attack import Attack
import numpy

class HomerAttack(Attack):
    '''
    classdocs
    '''


    def __init__(self, refMAF=None, caseMAF=None):
        '''
        Constructor
        '''
        self.refMAF = refMAF
        self.caseMAF = caseMAF 
    
    def getAttackStatistic(self, numOfSNPs, victimSeq):
        diffRef = 0
        diffCase = 0
        for i in range(numOfSNPs):
            diffRef += abs(victimSeq[i]/2.0 - self.refMAF[i])
            diffCase += abs(victimSeq[i]/2.0 - self.caseMAF[i])
        D = diffRef - diffCase
        return D
    
    def loadData(self, refMAFName, caseMAFName):
        refMAFFile = open(refMAFName)
        self.refMAF = [float(line.split()[1]) for line in refMAFFile]
        caseMAFFile = open(caseMAFName)
        self.caseMAF = [float(line.split()[1]) for line in caseMAFFile]

def performAttack(numOfVictims, numOfSNPs, sanitizationSuffix):
    attack = HomerAttack()
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
    
    file = open("../../data/simulated/attackStats/caseAttackStats_" + sanitizationSuffix + "_" +  str(numOfSNPs) + "SNPs.txt", 'w')
    file.write('\n'.join([str(x) for x in caseStats]))
    file.close()
    file = open("../../data/simulated/attackStats/testAttackStats_" + sanitizationSuffix + "_" +  str(numOfSNPs) + "SNPs.txt", 'w')
    file.write('\n'.join([str(x) for x in testStats]))
    file.close()

def calFalsePositive(caseStatsName, testStatsName):
    caseStatsFile = open(caseStatsName)
    testStatsFile = open(testStatsName)
    caseStats = numpy.array([float(line) for line in caseStatsFile])
    testStats = numpy.array([float(line) for line in testStatsFile])
    falsePositives = numpy.zeros(numpy.shape(testStats))
    falsePositives[testStats >= min(caseStats)] = 1
    return sum(falsePositives) / len(testStats)
    
    
if __name__ == "__main__":
    import sys
    arg = sys.argv
    performAttack(1000, int(arg[1]), arg[2])
    
#     performAttack(3, 10, "")
#     print calFalsePositive("../../data/simulated/caseAttackStats.txt", "../../data/simulated/testAttackStats.txt")
#     print calFalsePositive("../../data/simulated/caseAttackStats_dp0.1.txt", "../../data/simulated/testAttackStats_dp0.1.txt")
#     print calFalsePositive("../../data/simulated/caseAttackStats_dp0.05.txt", "../../data/simulated/testAttackStats_dp0.05.txt")
