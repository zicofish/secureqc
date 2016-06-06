'''
Created on Jun 1, 2016

@author: zhihuang
'''

def p_z_aggregator(namePrefix, n):
    outFile = open(namePrefix, 'w', 5000000)
    dummyLine = "2.0\t\t1.0000000475576258\n"
    for i in range(n):
        inFile = open(namePrefix + "." + str(i))
        for line in inFile.readlines():
            if line != dummyLine:
                outFile.write(line)
            else:
                break
    outFile.flush()
    outFile.close()
    
if __name__ == "__main__":
    p_z_aggregator("../../run/out/P_Z_1024.out", 2)