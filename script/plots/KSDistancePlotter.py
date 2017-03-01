'''
Created on Feb 16, 2017

@author: zhihuang
'''

import numpy
from plots.Plotter import Plotter
from scipy.stats import ks_2samp

class KDDistancePlotter(Plotter):
    
    numOfSNPs = numpy.array([1000, 5000, 10000, 50000, 100000, 500000, 1000000])
    numOfSNPsLabels = ['$10^3$', r'$5\times 10^3$', '$10^4$', r'$5\times 10^4$', '$10^5$', r'$5\times 10^5$', '$10^6$']
    plotMarkers = ["o", "^", "s", "+", "*", "h", "x", "D", "."]
    plotLabels = ["No noise", r'$\epsilon=0.1, \delta=0.05$', r'$\epsilon=0.1, \delta=0.01$', 
                  r'$\epsilon=0.1, \delta=0.005$', r'$\epsilon=0.1, \delta=0.001$',
                  r'$\epsilon=0.05, \delta=0.05$', r'$\epsilon=0.05, \delta=0.01$',
                  r'$\epsilon=0.05, \delta=0.005$', r'$\epsilon=0.05, \delta=0.001$']
    plotColors = ["red", "blue", "green", "magenta", "cyan", "yellow", "black", "orange", "brown"]

    
    def __init__(self, fileNames):
        '''
        Constructor
        '''
        self.fileNames = fileNames
        
    def plot(self):
        fig = Plotter.createFigure(self)
        ax = fig.add_subplot(1, 1, 1)
        for i in range(len(self.fileNames)):
            ksDist = []
            for j in range(len(self.fileNames[i])):
                caseFile = open(self.fileNames[i][j][0])
                testFile = open(self.fileNames[i][j][1])
                caseStats = [float(line) for line in caseFile.readlines()]
                testStats = [float(line) for line in testFile.readlines()]
                ksDist.append(ks_2samp(caseStats, testStats)[0])
            ax.plot(numpy.log10(self.numOfSNPs), ksDist, marker=self.plotMarkers[i], c=self.plotColors[i], label=self.plotLabels[i])
        ax.set_xlabel("Number of SNVs", fontsize=20)
        ax.set_ylabel("KS Distance", fontsize=20)
        ax.tick_params(axis='y', labelsize=20)
        ax.set_xticklabels(map(lambda x: '$10^{'+str(x)+'}$', ax.get_xticks()), fontsize=20)
        ax.set_ylim((0, 1))
        ax.legend(bbox_to_anchor=(1.05, 1.),
                  loc='upper left',
                  ncol=1,
                  borderaxespad=0.,
                  fontsize=18)
        
if __name__ == "__main__":
    plotter = KDDistancePlotter([
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_1000000SNPs.txt"]
                            ],
                            [
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_1000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_5000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_10000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_50000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_100000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_500000SNPs.txt"],
                                ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_1000000SNPs.txt"]
                            ]
                            ])
    plotter.plot()
    plotter.show()