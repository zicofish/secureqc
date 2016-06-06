'''
Created on May 9, 2016

@author: zhihuang
'''
import matplotlib.pyplot as plt

class PairPlotter(object):
    '''
    classdocs
    '''


    def __init__(self, data1 = None, data2 = None):
        '''
        Constructor
        '''
        self.data1 = data1
        self.data2 = data2
        
    def loadData(self, data1Name, data2Name):
        data1File = open(data1Name)
        self.data1 = [float(line.split()[1]) for line in data1File]
        data2File = open(data2Name)
        self.data2 = [float(line.split()[1]) for line in data2File]
        
    def plot(self, label1, label2):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
#         h = ax.scatter(self.data1[:10000], self.data2[:10000], marker='o', s = 5, c='blue', lw = 0)
        h = ax.scatter(self.data1, self.data2, marker='o', s = 5, c='blue', lw = 0)
        ax.set_xlabel(label1, fontsize=16)
        ax.set_ylabel(label2, fontsize=16)
        
        plt.show()


        
if __name__ == "__main__":
    plotter = PairPlotter()
#     plotter.loadData("../../data/simulated/caseMAF_dp0.05.txt", "../../data/simulated/refMAF.txt")
    plotter.loadData("../../data/simulated/caseMAF_dp0.1_delta0.01.txt", "../../data/simulated/refMAF.txt")
#     plotter.loadData("../../data/simulated/caseMAF_dp0.05_delta0.001.txt", "../../data/simulated/refMAF.txt")
#     plotter.loadData("../../data/simulated/caseMAF_dp0.1_delta0.05.txt", "../../data/simulated/refMAF.txt")
#     plotter.loadData("../../data/simulated/caseMAF_clear.txt", "../../data/simulated/refMAF.txt")
    plotter.plot("Case Allele Frequency", "Reference Allele Frequency")