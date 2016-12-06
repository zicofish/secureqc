'''
Created on May 11, 2016

@author: zhihuang
'''
import numpy
from plots.Plotter import Plotter

class GroupOfClasseseBoxPlotter(Plotter):
    '''
    classdocs
    '''


    def __init__(self, data = None):
        '''
        Constructor
        '''
        self.data = data
    
    
    def loadData(self, classNames):
        '''
        classNames a list of list of file names
        [
            [class1, class2, ..., classk]
            ...
            [class1, class2, ..., classk]
        ]
        '''
        self.numOfGroups = len(classNames)
        self.numOfClasses = len(classNames[0])
        self.data = []
        for i in range(self.numOfGroups):
            self.data.append([])
            minDatum = 1000000000
            maxDatum = -1000000000
            for j in range(self.numOfClasses):
                f = open(classNames[i][j])
                raw = [float(line) for line in f]
                tmp = min(raw)
                if tmp < minDatum:
                    minDatum = tmp
                tmp = max(raw)
                if tmp > maxDatum:
                    maxDatum = tmp
                self.data[i].append(raw)
                f.close()
            self.data[i] = (numpy.mat(self.data[i]).transpose() - minDatum) / (maxDatum - minDatum)
    
    def plot(self, classColors, groupLabels, xLabel, yLabel):
        fig = Plotter.createFigure(self)
        ax = fig.add_subplot(1,1,1)
        bps = []
        groupSpacing = 2
        for i in range(self.numOfGroups):
            pos = range(i*(self.numOfClasses + groupSpacing), 
                        (i+1)*(self.numOfClasses + groupSpacing)-2)
            bp = ax.boxplot(self.data[i], whis = [1, 99], positions = pos, widths=0.8, patch_artist = True)
            for j, box in enumerate(bp['boxes']):
                box.set(facecolor = classColors[j])
            bps.append(bp)
        ax.set_xlim(-2, self.numOfGroups*(self.numOfClasses + groupSpacing))
        
        ax.set_xlabel(xLabel, fontsize=20)
        ax.set_ylabel(yLabel, fontsize=20)
         
        ax.tick_params(axis='y', labelsize=20)
        ax.set_xticks(numpy.array(range(0, 
                         self.numOfGroups*(self.numOfClasses + groupSpacing), self.numOfClasses + groupSpacing)) + 0.5)
        ax.set_xticklabels(groupLabels, fontsize=18)
#         ax.set_xticklabels([])
#         ax.set_yticklabels([])
        return bps
        
if __name__ == "__main__":
    plotter = GroupOfClasseseBoxPlotter()
#     plotter.loadData([
#                     ["../../data/simulated/caseAttackStats_1000SNPs_clear.txt", "../../data/simulated/testAttackStats_1000SNPs_clear.txt"],
#                     ["../../data/simulated/caseAttackStats_5000SNPs_clear.txt", "../../data/simulated/testAttackStats_5000SNPs_clear.txt"],
#                     ["../../data/simulated/caseAttackStats_10000SNPs_clear.txt", "../../data/simulated/testAttackStats_10000SNPs_clear.txt"],
#                     ["../../data/simulated/caseAttackStats_50000SNPs_clear.txt", "../../data/simulated/testAttackStats_50000SNPs_clear.txt"],
#                     ["../../data/simulated/caseAttackStats_100000SNPs_clear.txt", "../../data/simulated/testAttackStats_100000SNPs_clear.txt"],
#                     ["../../data/simulated/caseAttackStats_500000SNPs_clear.txt", "../../data/simulated/testAttackStats_500000SNPs_clear.txt"],
#                       ["../../data/simulated/caseAttackStats_1000000SNPs_clear.txt", "../../data/simulated/testAttackStats_1000000SNPs_clear.txt"]
#                       ])
#     plotter.plot(["red", "blue"])
#     
    plotter.loadData([
                    ["../../data/simulated/caseAttackStats_1000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_1000SNPs_dp0.1.txt"],
                    ["../../data/simulated/caseAttackStats_5000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_5000SNPs_dp0.1.txt"],
                    ["../../data/simulated/caseAttackStats_10000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_10000SNPs_dp0.1.txt"],
                    ["../../data/simulated/caseAttackStats_50000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_50000SNPs_dp0.1.txt"],
                    ["../../data/simulated/caseAttackStats_100000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_100000SNPs_dp0.1.txt"],
                    ["../../data/simulated/caseAttackStats_500000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_500000SNPs_dp0.1.txt"],
                      ["../../data/simulated/caseAttackStats_1000000SNPs_dp0.1.txt", "../../data/simulated/testAttackStats_1000000SNPs_dp0.1.txt"]
                      ])
    plotter.plot(["red", "blue"])
    
#     plotter.loadData([
#                     ["../../data/simulated/caseAttackStats_1000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_1000SNPs_dp0.05.txt"],
#                     ["../../data/simulated/caseAttackStats_5000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_5000SNPs_dp0.05.txt"],
#                     ["../../data/simulated/caseAttackStats_10000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_10000SNPs_dp0.05.txt"],
#                     ["../../data/simulated/caseAttackStats_50000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_50000SNPs_dp0.05.txt"],
#                     ["../../data/simulated/caseAttackStats_100000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_100000SNPs_dp0.05.txt"],
#                     ["../../data/simulated/caseAttackStats_500000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_500000SNPs_dp0.05.txt"],
#                       ["../../data/simulated/caseAttackStats_1000000SNPs_dp0.05.txt", "../../data/simulated/testAttackStats_1000000SNPs_dp0.05.txt"]
#                       ])
#     plotter.plot(["red", "blue"])