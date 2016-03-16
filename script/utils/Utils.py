'''
Created on Mar 14, 2016

@author: zhihuang
'''
import struct
import base64

def convertToFixedPoint(floatNumber, width, offset):
    fixedPoint = int(floatNumber * (1 << offset)) & ((1 << width) - 1)
    return fixedPoint

def packToBase64(fixPointNumber, width):
    assert(width == 32 or width == 64) # We only handle these two widths
    if width == 32:
        typeStr = "I"
    else:
        typeStr = "Q"
    s = struct.pack("<"+typeStr, fixPointNumber)
    return base64.b64encode(s)

if __name__ == "__main__":
    floatNumber = float("8.851200e-01")
    width = 64
    offset = 62
    fp = convertToFixedPoint(floatNumber, width, offset)
    
    a = base64.b64decode("O3/CwJ3rcyk=")
    a = struct.unpack("<q", a)[0]
    
    b = base64.b64decode("O5NJRCt3OFg=")
    b = struct.unpack("<q", b)[0]
    
    print "a: ", a
    print "b: ", b
    
    print "c: ", a ^ b
    print "fp: ", fp
    
    print "recover float: ", fp * 1.0 / (1 << offset)