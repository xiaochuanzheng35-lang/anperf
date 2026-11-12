import os

def getFixupFrameNumber(compMethodConfigDict, default=0):
    fixupFrameNumber = default
    if "fixupFrameNumber" in compMethodConfigDict.keys():
        fixupFrameNumber = int( compMethodConfigDict["fixupFrameNumber"] )
    return fixupFrameNumber

def getThreshold(compMethodConfigDict, default=0.5):
    threshold = 0.5
    if "threshold" in compMethodConfigDict.keys():
        threshold = float(compMethodConfigDict["threshold"])
    return threshold

def getDetectFrameNumber(compMethodConfigDict, default=5):
    detectFrameNum = default
    if "detectFrameNum" in compMethodConfigDict.keys():
        detectFrameNum = int(compMethodConfigDict["detectFrameNum"])
    return detectFrameNum

def getCharacterCount(compMethodConfigDict, default=0):
    getCharacterCount = default
    if "characterCount" in compMethodConfigDict.keys():
        getCharacterCount = int( compMethodConfigDict["characterCount"] )
    return getCharacterCount

def getMoveDirection(compMethodConfigDict, default="horizontal"):
    moveDirection = default
    if "moveDirection" in compMethodConfigDict.keys():
        moveDirection = compMethodConfigDict["moveDirection"]
    return moveDirection

def getReturnPoint(compMethodConfigDict, default="start"):
    returnPoint = default
    if "returnPoint" in compMethodConfigDict.keys():
        returnPoint = compMethodConfigDict["returnPoint"]
    return returnPoint

def getChangeTrend(compMethodConfigDict, default="speed"):
    changeTrend = default
    if "changeTrend" in compMethodConfigDict.keys():
        changeTrend = compMethodConfigDict["changeTrend"]
    return changeTrend
