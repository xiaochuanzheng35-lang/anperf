import numpy
from . import anaToolRollingMinimaFinder


def proc(numpyYarray, paddingLen, threshold, curveBottomMinNum, rollWinSize, debug_level):
    avgValue = numpy.mean(numpyYarray)
    minValue = numpy.min(numpyYarray)
    maxThreshold  = max( threshold, (avgValue-(avgValue-minValue)*0.1)) 
    stepThreshold = 0.02
    workThreshold = threshold - stepThreshold
    bottomIdxList = []
    if debug_level>0:
        print(f"Search curve bottom: rollWinSize={rollWinSize}, minNum={curveBottomMinNum}, startThreshold={threshold}, maxThreshold={maxThreshold}")
    while len(bottomIdxList)<curveBottomMinNum:
        workThreshold += stepThreshold
        if debug_level>0:
            print(f"Try threshold: {workThreshold}")
        if workThreshold>maxThreshold:
            return []
        bottomIdxList  = anaToolRollingMinimaFinder.rolling_minima( numpyYarray, workThreshold, rollWinSize )
    if bottomIdxList[0]<(paddingLen+4):
        bottomIdxList = numpy.delete(bottomIdxList, 0) 
    if debug_level>0:
        print(f"Found curve bottom list = {bottomIdxList}")
    return bottomIdxList
