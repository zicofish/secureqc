'''
Created on May 23, 2016

@author: zhihuang
'''
import matplotlib.pyplot as plt
import numpy
import logging

class EAF_Plotter(object):
    '''
    classdocs
    '''
        
    def loadRefCase(self, refAFName, caseName, IDIdx = 0, A1Idx = 1, A2Idx = 2, AF1Idx = 3):
        self.loadRef(refAFName)
        self.loadCase(caseName, IDIdx, A1Idx, A2Idx, AF1Idx)
        self.intersect()
    
    def loadRef(self, refAFName):
        refAFFile = open(refAFName)
        refAFFile.readline()
        self.refAF = dict(map(lambda u: (u[0], u[1:]), [line.split() for line in refAFFile.readlines()]))
        refAFFile.close()
    
    def loadCase(self, caseName, IDIdx, A1Idx, A2Idx, AF1Idx):
        caseFile = open(caseName)
        caseFile.readline()
        self.caseAF = map(lambda u: [u[IDIdx], u[A1Idx], u[A2Idx], u[AF1Idx]], [line.split() for line in caseFile.readlines()])
    
    def loadPairs(self, pairName):
        pairFile = open(pairName)
        self.pairs = numpy.array([map(float, line.split()) for line in pairFile.readlines()])
    
    def intersect(self):
        self.pairs = []
        for i in range(len(self.caseAF)):
            if not self.refAF.has_key(self.caseAF[i][0]):
                continue
            refSNP = self.refAF.get(self.caseAF[i][0])
            if refSNP[0].upper() == self.caseAF[i][1] and \
                refSNP[1].upper() == self.caseAF[i][2]:
                self.pairs.append([float(refSNP[2]), float(self.caseAF[i][3])])
            elif refSNP[0].upper() == self.caseAF[i][2] and \
                refSNP[1].upper() == self.caseAF[i][1]:
                self.pairs.append([1 - float(refSNP[2]), float(self.caseAF[i][3])])
            else:
                logging.error('File content error: ' 'SNP ' + self.caseAF[i][0] + ' has different alleles in the reference and case.')
                continue
        self.pairs = numpy.array(self.pairs)
            
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        h = ax.scatter(self.pairs[:, 0], self.pairs[:, 1], marker='o', s = 5, c='blue', lw = 0)
#         ax.set_xlabel("EAF .reference", fontsize=16)
#         ax.set_ylabel("EAF .study", fontsize=16)
        
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        plt.show()
        
if __name__ == "__main__":
    plotter = EAF_Plotter() 
    #===========================================================================
    # pattern a
    #===========================================================================
#     plotter.loadRefCase("../../data/reference/AlleleFreq_HapMap_CEU.v2.SNPID.txt",
#                         "../../data/zk_jfellay/GIANT_toy/CLEAN.ARIC.HEIGHT.MEN.GT50.20100930.txt",
#                         0, 3, 4, 5)
    #===========================================================================
    # slight pattern c
    #===========================================================================
#     plotter.loadCase("../../data/reference/AlleleFreq_HapMap_CEU.v2.SNPID.txt",
#                         "../../data/zk_jfellay/GIANT_toy/SHIP-Trend.HEIGHT.MEN.GT50.20120228.txt",
#                         0, 3, 4, 5)
    #===========================================================================
    # pattern b
    #===========================================================================
#     plotter.loadRefCase("../../data/reference/AlleleFreq_HapMap_CEU.v2.SNPID.txt",
#                         "../../data/zk_jfellay/GIANT_toy/DESIR.HEIGHT.MEN.LE50.20120307.txt",
#                         0, 3, 4, 5)

    plotter.loadRefCase("../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt",
                          "../../data/simulated/eaf_patterns/e.txt")
#     plotter.loadPairs("../../data/output/eaf_plot_mpc_pattern_e_epsilon0.05_delta0.005_precision9_pairs155331.txt")
    plotter.plot()