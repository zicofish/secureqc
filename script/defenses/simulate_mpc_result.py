'''
Created on May 23, 2016

@author: zhihuang
'''

import logging
import numpy
from defenses.DifferentialPrivacy import DifferentialPrivacy
from utils import Utils

def sim_eaf(refAFName, studyAFName, outName, IDIdx = 0, A1Idx = 1, A2Idx = 2, AF1Idx = 3):
    #===========================================================================
    # reference allele frequencies
    #===========================================================================
    refAFFile = open(refAFName)
    refAFFile.readline()
    refAF = dict(map(lambda u: (u[0], u[1:]), [line.split() for line in refAFFile.readlines()]))
    refAFFile.close()
    
    #===========================================================================
    # study allele frequencies
    #===========================================================================
    studyAFFile = open(studyAFName)
    studyAFFile.readline()
    studyAF = map(lambda u: [u[IDIdx], u[A1Idx], u[A2Idx], u[AF1Idx]], [line.split() for line in studyAFFile.readlines()])
    studyAFFile.close()
    
    #===========================================================================
    # intersect
    #===========================================================================
    pairs = []
    for i in range(len(studyAF)):
        if not refAF.has_key(studyAF[i][0]):
            continue
        refSNP = refAF.get(studyAF[i][0])
        if refSNP[0].upper() == studyAF[i][1] and \
            refSNP[1].upper() == studyAF[i][2]:
            pairs.append([float(refSNP[2]), float(studyAF[i][3])])
        elif refSNP[0].upper() == studyAF[i][2] and \
            refSNP[1].upper() == studyAF[i][1]:
            pairs.append([1 - float(refSNP[2]), float(studyAF[i][3])])
        else:
            logging.error('File content error: ' 'SNP ' + studyAF[i][0] + ' has different alleles in the reference and case.')
            continue
    pairs = numpy.array(pairs)
    
    #===========================================================================
    # add noise
    #===========================================================================
    sensitivity = 1.0 / 1000
    epsilon = 0.1
    delta = 0.05
    dp = DifferentialPrivacy(sensitivity, epsilon, delta)
    noisy = dp.sanitize(pairs[:, 1], "gaussian")
    noisy = dp.sanitize(noisy, "gaussian") # try adding twice the noise
    noisy[noisy < 0.0] = 0.0
    noisy[noisy > 1.0] = 1.0
    pairs[:, 1] = noisy
    
    #===========================================================================
    # truncate precision
    #===========================================================================
    width = 32
    offset = 30
    precision = 7
    for i in range(len(pairs)):
        fp1 = Utils.convertToFixedPoint(pairs[i][0], width, offset)
        fp1 &= ((1 << (precision + width - offset)) - 1) << (offset - precision)
        fp2 = Utils.convertToFixedPoint(pairs[i][1], width, offset)
        fp2 &= ((1 << (precision + width - offset)) - 1) << (offset - precision)
        pairs[i] = [fp1, fp2]
        
    #===========================================================================
    # de-duplicate
    #===========================================================================
    def pairCmp(pair1, pair2):
        if pair1[0] < pair2[0]:
            return -1
        if pair1[0] > pair2[0]:
            return 1
        if pair1[1] < pair2[1]:
            return -1
        if pair1[1] > pair2[1]:
            return 1
        return 0
    pairs = sorted(pairs, pairCmp)
    newPairs = [pairs[0]]
    curPair = pairs[0]
    for i in range(1, len(pairs)):
        if pairCmp(curPair, pairs[i]) != 0:
            newPairs.append(pairs[i])
            curPair = pairs[i]
    
    
    #===========================================================================
    # output pairs
    #===========================================================================
    outFile = open(outName, 'w')
    outFile.write("\n".join(["\t".join(map(lambda u: str(Utils.convertToFloatPoint(u, width, offset)) , p)) for p in newPairs]))
    outFile.close()
    
if __name__ == "__main__":
    sim_eaf("../../data/reference/AlleleFreq_HapMap_CEU_phase3.2_nr.b36_fwd.txt",
            "../../data/simulated/eaf_patterns/b.txt",
            "../../data/output/eaf_plot_mpc_pattern_b.txt")
