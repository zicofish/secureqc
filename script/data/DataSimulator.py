'''
Created on Apr 29, 2016

@author: zhihuang
'''

import math
import random
import numpy

class DataSimulator(object):
    '''
    classdocs
    '''


    def __init__(self, n = 0, m = 0):
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
        
    def simStudyEAF(self, pattern, outName, hapmapAFName1, hapmapAFName2 = None):
        studyAF = []
        hapmapAFFile1 = open(hapmapAFName1)
        header = hapmapAFFile1.readline()
        hapmapAF1 = map(lambda u: [u[0], u[1], u[2], float(u[3])], [line.split() for line in hapmapAFFile1.readlines()])
        hapmapAFFile1.close()
        refAF1 = numpy.array([u[3] for u in hapmapAF1])
        gaussian_scale = 0.01
        if pattern == 'a':
            gaussian_scale = 0.01
            studyAF = refAF1 + numpy.random.normal(scale = gaussian_scale, size = len(refAF1))
            studyAF[studyAF < 0.001] = refAF1[studyAF < 0.001]
            studyAF[studyAF > 0.999] = refAF1[studyAF > 0.999]
        elif pattern == 'b':
            gaussian_scale = 0.05
            studyAF = refAF1 + numpy.random.normal(scale = gaussian_scale, size = len(refAF1))
            studyAF[studyAF < 0.001] = refAF1[studyAF < 0.001]
            studyAF[studyAF > 0.999] = refAF1[studyAF > 0.999]
        elif pattern == 'c':
            gaussian_scale = 0.03
            studyAF = refAF1 + numpy.random.normal(scale = gaussian_scale, size = len(refAF1))
            
            hapmapAFFile2 = open(hapmapAFName2)
            hapmapAFFile2.readline()
            hapmapAF2 = dict(map(lambda u: (u[0], float(u[3])), [line.split() for line in hapmapAFFile2.readlines()]))
            hapmapAFFile2.close()
            
            AF2Percentage = 0.008
            for i in range(len(hapmapAF1)):
                id = hapmapAF1[i][0]
                if not hapmapAF2.has_key(id):
                    continue
                r = numpy.random.uniform()
                if r <= AF2Percentage:
                    studyAF[i] = hapmapAF2.get(id)
            studyAF[studyAF < 0.001] = refAF1[studyAF < 0.001]
            studyAF[studyAF > 0.999] = refAF1[studyAF > 0.999]
        elif pattern == 'd':
            gaussian_scale = 0.03
            studyAF = refAF1 + numpy.random.normal(scale = gaussian_scale, size = len(refAF1))
            studyAF = 1 - studyAF
            studyAF[studyAF < 0.001] = 1 - refAF1[studyAF < 0.001]
            studyAF[studyAF > 0.999] = 1 - refAF1[studyAF > 0.999]
        elif pattern == 'e':
            gaussian_scale = 0.03
            studyAF = refAF1 + numpy.random.normal(scale = gaussian_scale, size = len(refAF1))
            reversedPercentage = 0.5
            reverse = [numpy.random.uniform(size = len(studyAF)) <= reversedPercentage]
            studyAF[reverse] = 1 - studyAF[reverse]
            studyAF[studyAF < 0.001] = refAF1[studyAF < 0.001]
            studyAF[studyAF > 0.999] = refAF1[studyAF > 0.999]
        
        studyAF = map(lambda x, y: [x[0], x[1], x[2], str(y)], hapmapAF1, studyAF)
        outFile = open(outName, 'w')
        outFile.write(header)
        outFile.write("\n".join(["\t".join(line) for line in studyAF]))
        outFile.close()
            
        
        
def simRefMAF(m, refMAFName):
    refMAF = open(refMAFName, 'w')
    mafs = ["SNP" + str(i) + "\t" + str(random.uniform(0.05, 0.5)) for i in range(m)]
    refMAF.write('\n'.join(mafs))
    
        
if __name__ == "__main__":
#     simRefMAF(3000000, "../../data/simulated/refMAF.txt")
#     simulator = DataSimulator(1000, 3000000)
#     simulator.loadRefMAF("../../data/simulated/refMAF.txt")
#     simulator.generate("../../data/simulated/test.txt", "../../data/simulated/testMAF.txt")
    simulator = DataSimulator()
#     simulator.simStudyEAF('a', "../../data/simulated/eaf_patterns/a.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CHB_phase3.2_nr.b36_fwd.txt")
#     simulator.simStudyEAF('b', "../../data/simulated/eaf_patterns/b.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CHB_phase3.2_nr.b36_fwd.txt")
#     simulator.simStudyEAF('c', "../../data/simulated/eaf_patterns/c.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CHB_phase3.2_nr.b36_fwd.txt")
#     simulator.simStudyEAF('d', "../../data/simulated/eaf_patterns/d.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt", 
#                           "../../data/reference/AlleleFreq_HapMap_CHB_phase3.2_nr.b36_fwd.txt")
    simulator.simStudyEAF('e', "../../data/simulated/eaf_patterns/e.txt", 
                          "../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt", 
                          "../../data/reference/AlleleFreq_HapMap_CHB_phase3.2_nr.b36_fwd.txt")
    