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


    def __init__(self, sensitivity, epsilon, delta):
        '''
        Constructor
        '''
        self.sensitivity = sensitivity
        self.epsilon = epsilon
        self.delta = delta
        
    def setSensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
        
    def setDelta(self, delta):
        self.delta = delta
    
    def sanitize(self, data, method="laplacian"):
        noises = numpy.zeros(len(data))
        if method == "laplacian":
            noises = numpy.random.laplace(scale = self.sensitivity / self.epsilon, size = len(data))
        elif method == "gaussian":
            c = numpy.sqrt(2*numpy.log(1.25/self.delta))
            std = c*self.sensitivity / self.epsilon
            noises = numpy.random.normal(scale = std, size = len(data))
        return numpy.array(data) + noises
    
def addLaplacianNoises():
    caseMAF = open("../../data/simulated/caseMAF_clear.txt")
    mafs = [float(line.split()[1]) for line in caseMAF]
    sensitivity = 1.0/1000
    epsilon = 1
    dp = DifferentialPrivacy(sensitivity, epsilon)
    noisy = dp.sanitize(mafs, "laplacian")
    noisy[noisy < 0.05] = 0.05
    noisy[noisy > 0.95] = 0.95
    noisyMAF = open("../../data/simulated/caseMAF_dp" + str(epsilon) + ".txt", 'w')
    noisyMAF.write('\n'.join(["SNP" + str(i) + "\t" + str(noisy[i]) for i in range(len(noisy))]))
    noisyMAF.close()
    
def addGaussianNoises():
    caseMAF = open("../../data/simulated/caseMAF_clear.txt")
    mafs = [float(line.split()[1]) for line in caseMAF]
    sensitivity = 1.0/1000
    epsilon = 0.05
    delta = 0.005
    dp = DifferentialPrivacy(sensitivity, epsilon, delta)
    noisy = dp.sanitize(mafs, "gaussian")
    noisy[noisy < 0.05] = 0.05
    noisy[noisy > 0.95] = 0.95
    noisyMAF = open("../../data/simulated/caseMAF_dp" + str(epsilon) + "_delta" + str(delta) + ".txt", 'w')
    noisyMAF.write('\n'.join(["SNP" + str(i) + "\t" + str(noisy[i]) for i in range(len(noisy))]))
    noisyMAF.close()

if __name__ == "__main__":
#     addLaplacianNoises()
    addGaussianNoises()
        