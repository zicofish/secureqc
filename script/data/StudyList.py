'''
Created on Mar 14, 2016

@author: zhihuang
'''
def listStudyFiles(inputDir, ending, outName):
    from os import listdir
    from os.path import isfile, join
    files = [join(inputDir, f) for f in listdir(inputDir) if (isfile(join(inputDir, f)) and f.endswith(ending))]
    out = open(outName, "w")
    out.write("\n".join(files))
    out.flush()
    out.close()
    
if __name__ == "__main__":
    listStudyFiles("../../data/zk_jfellay/GIANT_toy/small", ".small.A.txt", "../../data/study_list.gen.small.txt")
    listStudyFiles("../../data/zk_jfellay/GIANT_toy/small", ".small.B.txt", "../../data/study_list.eva.small.txt")