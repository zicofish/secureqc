'''
Created on Feb 24, 2016

@author: zhihuang
'''

import matplotlib.pyplot as plt
import numpy

class SE_N_Plotter(object):
    """
    The class for plotting the SE-N plot in the meta-level QC of meta-analysis 
    """
    

    def __init__(self, data = None):
        '''
        Construct the plotter with two-dimensional data of the form:
        [ 
            [sqrt(Nmax), 1.93/median(SE)],
            ...
        ]
        '''
        self.data = data
    
    def plot(self):
        '''
        Notes: Before calling this function, data must be loaded, either through
        the constructor, or through the function 'loadData'.
        '''
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        h = ax.scatter(self.data[:, 0], self.data[:, 1], marker='o', s = 50, c='blue')
        ax.set_xlabel('Sqrt(Nmax)', fontsize=16)
        ax.set_ylabel('1.93/median(SE)', fontsize=16)
        
        plt.show()

    def loadData(self, SE_N_FileName):
        se_n_file = open(SE_N_FileName)
        se_n_file.readline()
        self.data = [map(float, line.split()[1:]) for line in se_n_file.readlines()]
        self.data = numpy.array(self.data)
        self.data[:, 0] = numpy.sqrt(self.data[:, 0])
        calibrationFactor = 1.93
        self.data[:, 1] = calibrationFactor / self.data[:, 1]
        
if __name__ == "__main__":
    plotter = SE_N_Plotter()
    plotter.loadData("../..//data/output/SE_N_plot_data.txt")
    plotter.plot()