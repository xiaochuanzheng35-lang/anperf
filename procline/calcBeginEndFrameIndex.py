def getSpecItemInList(datalist, methodString):
    if   methodString=="max":        return max(datalist)
    elif methodString=="min":        return min(datalist)
    else:        return -1

def getSpecDataListByIndexList(datalist, indexlist):
    retlist = []
    for idx in indexlist:
        retlist.append( datalist[idx] )
    return retlist

#    "compBeginEndTimeConfDict" : {
#        "specStationIndexList"  :  [1, 2],
#        "beginTimeConfDict" : {
#            "method"         : "min",
#            "candidateList"  :  [0, 1]
#        },
#        "endTimeConfDict" : {
#            "method"         : "max",
#            "candidateList"  :  [1, 2]
#        }
#    }
def selectFromFrameIndexList(findFrameIdxList, calcMethodConfigDict):
    specListKey  = "specStationIndexList"
    beginTimeKey = "beginTimeConfDict"
    endTimeKey   = "endTimeConfDict"
    if specListKey in calcMethodConfigDict.keys():
        specStaLst = calcMethodConfigDict[ specListKey ]
        tmpBegIdx  = specStaLst[0]
        tmpEndIdx  = specStaLst[1]
        if len(findFrameIdxList)>tmpEndIdx:
            realBeginFrameIdx = findFrameIdxList[tmpBegIdx]
            realEndFrameIndex = findFrameIdxList[tmpEndIdx]
            return [realBeginFrameIdx, realEndFrameIndex]
    elif (beginTimeKey in calcMethodConfigDict.keys()) and (endTimeKey in calcMethodConfigDict.keys()):
        tmplist = getSpecDataListByIndexList( findFrameIdxList, calcMethodConfigDict[ beginTimeKey ]["candidateList"] )
        print(tmplist)
        realBeginFrameIdx = getSpecItemInList( tmplist, calcMethodConfigDict[ beginTimeKey ]["method"] )
        tmplist = getSpecDataListByIndexList( findFrameIdxList, calcMethodConfigDict[ endTimeKey ]["candidateList"] )
        print(tmplist)
        realEndFrameIndex = getSpecItemInList( tmplist, calcMethodConfigDict[ endTimeKey ]["method"] )
        return [realBeginFrameIdx, realEndFrameIndex]
    return []

