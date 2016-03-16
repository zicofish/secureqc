'''
Created on Mar 9, 2016

@author: zhihuang
'''

class DataCropper(object):
    '''
    Crop the first n rows in the data file. It can be used to generate small datasets.
    '''


    def __init__(self, n):
        '''
        Initialize with n indicating the number of rows to crop
        '''
        self.n = n
    
    def cropFile(self, inFilePath, outFilePath):
        inFile = open(inFilePath)
        outFile = open(outFilePath, 'w')
        nRows = inFile.readlines()[:self.n]
        outFile.write("".join(nRows))
        outFile.close()
        inFile.close()
        
    def cropFilesInDir(self, inDirPath, outDirPath, filePatternStr):
        from os import listdir
        from os.path import isfile, join
        import re
        filePattern = re.compile(filePatternStr)
        inFiles = [f for f in listdir(inDirPath) if (isfile(join(inDirPath, f)) and filePattern.match(f) != None)]
        for f in inFiles:
            self.cropFile(join(inDirPath, f), join(outDirPath, f[:-4] + ".small" + f[-4:]))

if __name__ == "__main__":
    cropper = DataCropper(1001)
    cropper.cropFilesInDir("../../data/zk_jfellay/GIANT_toy", "../../data/zk_jfellay/GIANT_toy/small", r".*\.txt$")