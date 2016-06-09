'''
Created on Mar 9, 2016

@author: zhihuang
'''

import random
from utils import Utils

class DataSplitter(object):
    '''
    Split data in two shares.
    '''
    #===========================================================================
    # Columns of a study file
    #===========================================================================
    headers = ["MarkerName",
        "Strand",
        "N",
        "Effect_allele",
        "Other_allele",
        "EAF",
        "Imputation",
        "Information_type",
        "Information",
        "BETA",
        "SE",
        "P",
        "MAC"];
    
    #===========================================================================
    # We use fix-point representation for the data fields that need to be shared.
    # 1 bit reserved for sign.
    # EAF (index: 5) is in [0, 1]. Use 30 bits for the fractional part, 1 bit for the integral part (not necessary, but we don't want to deal with 1<<31, which is a negative integer in Java). 
    # BETA (index: -4). Assume 7 bits for integral part, 24 bits for fractional part.
    # SE (index: -3). Assume 7 bits for integral part, 24 bits for fractional part. 
    # P value (index: -2), in [0, 1]. Use 62 bits for the fractional part, 1 bit for the integral part (not necessary, but we don't want to deal with 1<<63, which is a negative long in Java).
    #===========================================================================
    index = [5, -4, -3, -2]
    width = [32, 32, 32, 64]
    offset = [30, 24, 24, 62]
        
    def splitFile(self, inFilePath):
        inFile = open(inFilePath)
        outFileA = open(inFilePath + ".alice", 'w')
        outFileB = open(inFilePath + ".bob", 'w')
        # Skip header line
        headerLine = inFile.readline()
        outFileA.write(headerLine)
        outFileB.write(headerLine)
        for line in inFile.readlines():
            fields = line.split()
            fieldsA = [x for x in fields]
            fieldsB = [x for x in fields]
            # Split EAF, BETA, SE, and P value into two shares with fix-point representation
            for i in range(len(self.index)):
                fp = Utils.convertToFixedPoint(
                                              float(fields[self.index[i]]), 
                                              self.width[i], 
                                              self.offset[i])
                r = random.getrandbits(self.width[i])
                
                fieldsA[self.index[i]] = Utils.packToBase64(r, self.width[i])
                fieldsB[self.index[i]] = Utils.packToBase64(fp ^ r, self.width[i])
                
            outFileA.write("\t".join(fieldsA) + "\n")
            outFileB.write("\t".join(fieldsB) + "\n")
        outFileA.flush()
        outFileA.close()
        outFileB.flush()
        outFileB.close()
        inFile.close()
    
if __name__ == "__main__":
    splitter = DataSplitter()
#     splitter.splitFile("../../data/zk_jfellay/GIANT_toy/small/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.small.txt")
    splitter.splitFile("../../data/zk_jfellay/GIANT_toy/CLEAN.AGES.HEIGHT.MEN.GT50.20100914.txt")