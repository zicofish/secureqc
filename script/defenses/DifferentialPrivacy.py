'''
Created on May 8, 2016

@author: zhihuang
'''
from defenses.Defense import Defense
import numpy

class DifferentialPrivacy(Defense):
    '''
    classdocs
    '''


    def __init__(self, sensitivity, epsilon):
        '''
        Constructor
        '''
        self.sensitivity = sensitivity
        self.epsilon = epsilon
        
    def setSensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    
    def sanitize(self, data):
        noises = numpy.random.laplace(scale = self.sensitivity / self.epsilon, size = len(data))
        return numpy.array(data) + noises
    
if __name__ == "__main__":
    caseMAF = open("../../data/simulated/caseMAF.txt")
    mafs = [float(line.split()[1]) for line in caseMAF]
    sensitivity = 1.0/1000
    epsilon = 1
    dp = DifferentialPrivacy(sensitivity, epsilon)
    noisy = dp.sanitize(mafs)
    noisy[noisy < 0.05] = 0.05
    noisy[noisy > 0.95] = 0.95
    noisyMAF = open("../../data/simulated/caseMAF_dp" + str(epsilon) + ".txt", 'w')
    noisyMAF.write('\n'.join(["SNP" + str(i) + "\t" + str(noisy[i]) for i in range(len(noisy))]))
    noisyMAF.close()
        