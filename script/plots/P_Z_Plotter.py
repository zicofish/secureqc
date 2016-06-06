'''
Created on Feb 29, 2016

@author: zhihuang
'''
from plots.PairPlotter import PairPlotter
import numpy
from scipy import stats

class P_Z_Plotter(PairPlotter):
    '''
    classdocs
    '''
    
    def loadData(self, studyName, type="plain"):
        '''
        type can be 'plain' or 'secure'
        '''
        studyFile = open(studyName)
        if type == 'plain':
            studyFile.readline()
            data = numpy.array(map(lambda u: [float(u[-4]), float(u[-3]), float(u[-2])], [line.split() for line in studyFile.readlines()]))
            zStats = data[:, 0] / data[:, 1]
            computedPValues = stats.norm.sf(abs(zStats)) * 2
            originalPValues = data[:, 2]
            
        elif type == 'secure':
            data = numpy.array([map(float, line.split()) for line in studyFile.readlines()])
            originalPValues = data[:, 0]
            computedPValues = data[:, 1]
        self.data1 = - numpy.log10(computedPValues)
        self.data2 = - numpy.log10(originalPValues)
    
if __name__ == "__main__":
    plotter = P_Z_Plotter()
    plotter.loadData("../../data/zk_jfellay/GIANT_toy/small/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.small.txt")
#     plotter.loadData("../../run/out/P_Z_1024.out", "secure")
    plotter.plot(r'$-\log_{10}(P.ztest)$', r'$-\log_{10}(P)$')
    