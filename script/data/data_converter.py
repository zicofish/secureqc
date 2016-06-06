'''
Created on May 23, 2016

@author: zhihuang
'''

def mapChrPosAFToSNPIDAF(refAFName, newRefAFName, SNPIDMappingName):
    refAFFile = open(refAFName)
    newRefAFFile = open(newRefAFName, 'w')
    SNPIDMappingFile = open(SNPIDMappingName)
    
    refAFHeader = refAFFile.readline()  # Skip header
    refAF = [line.split() for line in refAFFile.readlines()]
    
    SNPIDMappingFile.readline()
    mapping = dict(map(lambda u: (u[0], u[1]), [line.split() for line in SNPIDMappingFile]))
    
    for i in range(len(refAF)):
        if not mapping.has_key(refAF[i][0]):
            continue
        refAF[i][0] = mapping.get(refAF[i][0])
    
    newRefAFFile.write(refAFHeader)
    newRefAFFile.write("\n".join(["\t".join(snp) for snp in refAF]))
    newRefAFFile.close()
    
    refAFFile.close()
    SNPIDMappingFile.close()
    
def combineHapmapAF(folder, ancestry):
    chrs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
            "14", "15", "16", "17", "18", "19", "20", "21", "22", "M", "X"]
    refAF = []
    for i in range(len(chrs)):
        chrAFFile = open(folder + "allele_freqs_chr" + chrs[i] + "_" + ancestry + "_phase3.2_nr.b36_fwd.txt")
        header = chrAFFile.readline().split()
        if i == 0:
            refAF.append([header[0], header[-7], header[-4], header[-6]])
        refAF.extend(map(lambda u: [u[0], u[-7], u[-4], u[-6]], [line.split() for line in chrAFFile.readlines()]))
        chrAFFile.close()
    outFile = open(folder + "AlleleFreq_HapMap_" + ancestry + "_phase3.2_nr.b36_fwd.txt", 'w')
    outFile.write("\n".join(["\t".join(line) for line in refAF]))
    outFile.close()
    
if __name__ == "__main__":
#     mapChrPosAFToSNPIDAF("../../data/reference/AlleleFreq_HapMap_CEU.v2.txt",
#                  "../../data/reference/AlleleFreq_HapMap_CEU.v2.SNPID.txt",
#                  "../../data/reference/SNPID_to_ChrPosID.b36_v2.txt")
#     combineHapmapAF("../../data/reference/", "CEU")
    combineHapmapAF("../../data/reference/", "CHB")
    