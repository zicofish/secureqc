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
                                                 xLabel="Number of SNVs", yLabel="Rescaled LLR statistics")
            false_positives = []
            for j, bp in enumerate(bps):
                threshold = bp['caps'][0].get_ydata()[0]
                false_positives.append(int((self.data[j][:, 1] >= threshold).sum()) * 1.0 / len(self.data[j][:, 1]))
            ax.plot(numpy.log10(self.numOfSNPs), false_positives, marker=self.plotMarkers[i], c=self.plotColors[i], label=self.plotLabels[i])
#             print false_positives
        ax.set_xlabel("Number of SNVs", fontsize=20)
        ax.set_ylabel("False positive rate", fontsize=20)
        ax.tick_params(axis='y', labelsize=20)
        ax.set_xticklabels(map(lambda x: '$10^{'+str(x)+'}$', ax.get_xticks()), fontsize=20)
        ax.legend(bbox_to_anchor=(1.05, 1.),
                  loc='upper left',
                  ncol=1,
                  borderaxespad=0.,
                  fontsize=18)
        fig.savefig("./test.pdf", format="pdf")
#         ax.set_xticks(numpy.log10(self.numOfSNPs))
#         ax.set_xticklabels(map(str, self.numOfSNPs))

if __name__ == "__main__":
#     plotter = FalsePositivePlotter([
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_clear.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_clear.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_clear.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.05.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.01.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.005.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.1_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.1_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.1_delta0.001.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.05.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.05.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.05.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.01.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.01.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.01.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.005.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.005.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.005.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_5000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_5000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_10000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_10000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_50000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_50000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_100000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_100000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_500000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_500000SNPs_dp0.05_delta0.001.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_1000000SNPs_dp0.05_delta0.001.txt", "../../data/simulated/attackStats/testAttackStats_1000000SNPs_dp0.05_delta0.001.txt"]
#                                 ]
#                                 ])
#     plotter = FalsePositivePlotter([
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_clear_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_clear_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_1000000SNPs.txt"]
#                                 ],
#                                 [
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_1000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_1000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_5000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_5000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_10000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_10000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_50000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_50000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_100000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_100000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_500000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_500000SNPs.txt"],
#                                     ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_1000000SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_1000000SNPs.txt"]
#                                 ]
#                                 ])
#     plotter = FalsePositivePlotter([
#                                 [
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.01_752SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.01_752SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.001_829SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.001_829SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.01_10024SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.01_10024SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.001_11084SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.001_11084SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.01_108856SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.01_108856SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.001_119132SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.001_119132SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.05_687SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.05_687SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.005_769SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.005_769SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.05_9128SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.05_9128SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.005_10355SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.005_10355SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.05_99617SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.05_99617SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.1_delta0.005_112151SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.1_delta0.005_112151SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.01_1008SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.01_1008SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.001_1067SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.001_1067SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.01_14095SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.01_14095SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.001_15282SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.001_15282SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.01_150914SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.01_150914SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.001_164068SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.001_164068SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.05_923SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.05_923SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.005_1037SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.005_1037SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.05_12840SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.05_12840SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.005_14535SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.005_14535SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.05_137365SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.05_137365SNPs.txt"],
#                                     ["../../data/simulated/attackStats/caseAttackStats_dp0.05_delta0.005_155331SNPs.txt", "../../data/simulated/attackStats/testAttackStats_dp0.05_delta0.005_155331SNPs.txt"],                                    
#                                 ]
#                                     ])
    plotter = FalsePositivePlotter([
                                [
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_752SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_752SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_829SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_829SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_10024SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_10024SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_11084SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_11084SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.01_108856SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.01_108856SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.001_119132SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.001_119132SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_687SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_687SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_769SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_769SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_9128SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_9128SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_10355SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_10355SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.05_99617SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.05_99617SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.1_delta0.005_112151SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.1_delta0.005_112151SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_1008SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_1008SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_1067SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_1067SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_14095SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_14095SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_15282SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_15282SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.01_150914SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.01_150914SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.001_164068SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.001_164068SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_923SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_923SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_1037SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_1037SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_12840SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_12840SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_14535SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_14535SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.05_137365SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.05_137365SNPs.txt"],
                                    ["../../data/simulated/attackStats/LLR_caseAttackStats_dp0.05_delta0.005_155331SNPs.txt", "../../data/simulated/attackStats/LLR_testAttackStats_dp0.05_delta0.005_155331SNPs.txt"],                                    
                                ]
                                    ])
    plotter.plot()
    plotter.show()
