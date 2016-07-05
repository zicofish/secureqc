'''
Created on May 9, 2016

@author: zhihuang
'''
import matplotlib.pyplot as plt
import numpy

class DataDeviationPlotter(object):
    '''
    classdocs
    '''
        
    def loadData(self, caseNames):
        originalCaseFile = open(caseNames[0])
        originalPoints = numpy.array([float(line.split()[1]) for line in originalCaseFile])
        originalCaseFile.close()
        self.deviations = []
        for i in range(1, len(caseNames)):
            noisyCaseFile = open(caseNames[i])
            noisyPoints = numpy.array([float(line.split()[1]) for line in noisyCaseFile])
            self.deviations.append(numpy.abs(noisyPoints - originalPoints).sum() / len(noisyPoints))
            
        
    def plot(self, label1, label2, tickLabels):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
#         h = ax.plot(range(len(self.deviations)), self.deviations, marker='o', c='blue')
        ax.bar(range(1, len(self.deviations) + 1), self.deviations, width = 0.6, color = 'gray')
        ax.set_xlabel(label1, fontsize=20)
        ax.set_ylabel(label2, fontsize=20)
        
        ax.tick_params(axis="y", labelsize=20)
        ax.set_xlim(left=0.6)
        ax.set_xticks(numpy.array(range(1, len(self.deviations) + 1)) + 0.3)
        ax.set_xticklabels(tickLabels, fontsize=20)
        
        plt.show()
        
if __name__ == "__main__":
    plotter = DataDeviationPlotter()
#     plotter.loadData(["../../data/simulated/caseMAF_clear.txt",
#                       "../../data/simulated/caseMAF_dp0.1.txt",
#                       "../../data/simulated/caseMAF_dp0.05.txt",
#                       "../../data/simulated/caseMAF_dp0.01.txt"])
    plotter.loadData(["../../data/simulated/caseMAF_clear.txt",
                      "../../data/simulated/caseMAF_dp0.1_delta0.05.txt",
                      "../../data/simulated/caseMAF_dp0.1_delta0.01.txt",
                      "../../data/simulated/caseMAF_dp0.1_delta0.005.txt",
                      "../../data/simulated/caseMAF_dp0.1_delta0.001.txt",
                      "../../data/simulated/caseMAF_dp0.05_delta0.05.txt",
                      "../../data/simulated/caseMAF_dp0.05_delta0.01.txt",
                      "../../data/simulated/caseMAF_dp0.05_delta0.005.txt",
                      "../../data/simulated/caseMAF_dp0.05_delta0.001.txt"])
    plotter.plot("Privacy parameter", "Average distance from true MAF",
                 ['$\epsilon=0.1$\n$\delta=0.05$', '$\epsilon=0.1$\n$\delta=0.01$', 
                  '$\epsilon=0.1$\n$\delta=0.005$', '$\epsilon=0.1$\n$\delta=0.001$',
                  '$\epsilon=0.05$\n$\delta=0.05$', '$\epsilon=0.05$\n$\delta=0.01$',
                  '$\epsilon=0.05$\n$\delta=0.005$', '$\epsilon=0.05$\n$\delta=0.001$'])