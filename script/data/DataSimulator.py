'''
Created on Apr 29, 2016

@author: zhihuang
'''

import math
import random

class DataSimulator(object):
    '''
    classdocs
    '''


    def __init__(self, n, m):
        '''
        Constructor
        '''
        self.studySize = n
        self.numOfSNPs = m
        
    def loadRefMAF(self, refMAFName):
        refMAF = open(refMAFName)
        self.mafs = [float(line.split()[1]) for line in refMAF]
        
    def generate(self, outGenotypeName, outMAFName):
        dataset = []
        outGenotype = open(outGenotypeName, 'w')
        outMAF = open(outMAFName, 'w')
        caseMAF = [0 for i in self.mafs]
        for i in range(self.studySize):
            dataset.append(["P" + str(i)])
            for j in range(self.numOfSNPs):
                s0 = (1 - self.mafs[j]) * (1 - self.mafs[j]) # 0 minor allele
                s1 = 2 * self.mafs[j] * (1 - self.mafs[j]) # 1 minor allele
                r = random.random()
                if r <= s0:
                    dataset[i].append('0')
                elif r <= s0 + s1:
                    dataset[i].append('1')
                    caseMAF[j] += 1
                else:
                    dataset[i].append('2')
                    caseMAF[j] += 2
            outGenotype.write('\t'.join(dataset[i]) + '\n')
        caseMAF = ["SNP" + str(i) + "\t" + str(caseMAF[i]*1.0/(2*self.studySize)) for i in range(len(caseMAF))]
        outMAF.write('\n'.join(caseMAF))
            
        outGenotype.close()
        outMAF.close()
        
def simRefMAF(m, refMAFName):
    refMAF = open(refMAFName, 'w')
    mafs = ["SNP" + str(i) + "\t" + str(random.uniform(0.05, 0.5)) for i in range(m)]
    refMAF.write('\n'.join(mafs))
    
        
if __name__ == "__main__":
#     simRefMAF(3000000, "../../data/simulated/refMAF.txt")
    simulator = DataSimulator(1000, 3000000)
    simulator.loadRefMAF("../../data/simulated/refMAF.txt")
    simulator.generate("../../data/simulated/test.txt", "../../data/simulated/testMAF.txt")