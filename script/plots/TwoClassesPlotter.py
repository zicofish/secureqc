'''
Created on May 9, 2016

@author: zhihuang
'''

import matplotlib.pyplot as plt

class TwoClassesPlotter(object):
    '''
    classdocs
    '''


    def __init__(self, class1 = None, class2 = None):
        '''
        Constructor
        '''
        self.class1 = class1
        self.class2 = class2
    
    def loadData(self, class1Name, class2Name):
        class1File = open(class1Name)
        self.class1 = [float(line) for line in class1File]
        class2File = open(class2Name)
        self.class2 = [float(line) for line in class2File]
        
    def plot(self, xlabel, ylabel):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        h1 = ax.scatter(range(len(self.class1)), 
                        self.class1, 
                        marker='o', s = 50, c='red')
        h2 = ax.scatter(range(len(self.class1), len(self.class1) + len(self.class2)), 
                        self.class2, 
                        marker='^', s = 50, c='green')
        ax.set_xlabel(xlabel, fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        
        plt.show()
        
if __name__ == "__main__":
    plotter = TwoClassesPlotter()
#     plotter.loadData("../../data/simulated/testAttackStats_dp0.1.txt", "../../data/simulated/caseAttackStats_dp0.1.txt")
    plotter.loadData("../../data/simulated/testAttackStats.txt", "../../data/simulated/caseAttackStats.txt")
#     plotter.loadData("../../data/simulated/testAttackStats_dp0.05.txt", "../../data/simulated/caseAttackStats_dp0.05.txt")
    plotter.plot("Participant Index", "Test Statistic")