'''
Created on May 11, 2016

@author: zhihuang
'''
from plots.GroupOfClassesBoxPlotter import GroupOfClasseseBoxPlotter
from plots.Plotter import Plotter
import numpy
import matplotlib.pyplot as plt

class FalsePositivePlotter(GroupOfClasseseBoxPlotter):
    '''
    classdocs
    '''
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
            GroupOfClasseseBoxPlotter.loadData(self, self.fileNames[i])
            bps = GroupOfClasseseBoxPlotter.plot(self, ["red", "blue"], 
                                                 groupLabels = self.numOfSNPsLabels,
                                                 xLabel="Number of SNVs", yLabel="Normalized D statistics")
            false_positives = []
            for j, bp in enumerate(bps):
                threshold = bp['caps'][0].get_ydata()[0]
                false_positives.append(int((self.data[j][:, 1] >= threshold).sum()) * 1.0 / len(self.data[j][:, 1]))
            ax.plot(numpy.log10(self.numOfSNPs), false_positives, marker=self.plotMarkers[i], c=self.plotColors[i], label=self.plotLabels[i])
        ax.set_xlabel("Number of SNVs", fontsize=20)
        ax.set_ylabel("False positive rate", fontsize=20)
        ax.tick_params(axis='y', labelsize=20)
        ax.set_xticklabels(map(lambda x: '$10^{'+str(x)+'}$', ax.get_xticks()), fontsize=20)
        ax.legend(bbox_to_anchor=(0.998, 0.65),
              fontsize=18)
#         ax.set_xticks(numpy.log10(self.numOfSNPs))
#         ax.set_xticklabels(map(str, self.numOfSNPs))
            
if __name__ == "__main__":
#     plotter = FalsePositivePlotter([
#                                     [
#                                         ["../../data/simulated/caseAttackStats_1000SNPs_clear.txt", "../../data/simulated/testAttackStats_1000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_5000SNPs_clear.txt", "../../data/simulated/testAttackStats_5000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_10000SNPs_clear.txt", "../../data/simulated/testAttackStats_10000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_50000SNPs_clear.txt", "../../data/simulated/testAttackStats_50000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_100000SNPs_clear.txt", "../../data/simulated/testAttackStats_100000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_500000SNPs_clear.txt", "../../data/simulated/testAttackStats_500000SNPs_clear.txt"],
#                                         ["../../data/simulated/caseAttackStats_1000000SNPs_clear.txt", "../../data/simulated/testAttackStats_1000000SNPs_clear.txt"]
#                                     ],
#                                     [
#                                         ["../../data/simulated/caseAttackStats_1000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_1000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_5000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_5000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_10000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_10000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_50000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_50000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_100000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_100000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_500000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_500000SNPs_dp0.1.txt"],
#                                         ["../../data/simulated/caseAttackStats_1000000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_1000000SNPs_dp0.1.txt"]
#                                     ],
#                                     [
#                                         ["../../data/simulated/caseAttackStats_1000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_1000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_5000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_5000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_10000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_10000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_50000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_50000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_100000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_100000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_500000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_500000SNPs_dp0.05.txt"],
#                                         ["../../data/simulated/caseAttackStats_1000000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_1000000SNPs_dp0.05.txt"]
#                                     ],
#                                     [
#                                         ["../../data/simulated/caseAttackStats_1000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_1000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_5000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_5000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_10000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_10000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_50000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_50000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_100000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_100000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_500000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_500000SNPs_dp0.01.txt"],
#                                         ["../../data/simulated/caseAttackStats_1000000SNPs_dp0.01.txt", "../../data/simulated/testAttackStats_1000000SNPs_dp0.01.txt"]
#                                     ]
#                                     ])
    plotter = FalsePositivePlotter([
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_clear.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_clear.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.05.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.01.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.005.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.001.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.05.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.05.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.01.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.01.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.005.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.005.txt"]
                                ],
                                [
                                    ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.001.txt"],
                                    ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.001.txt"]
                                ]
                                ])
    plotter.plot()
    plotter.show()