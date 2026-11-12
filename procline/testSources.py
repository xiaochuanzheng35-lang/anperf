import os, cv2
from tools import FolderOp

def getCaseIDFromRdsPath(rdsPath): # last folder name sample: <testName>_@_<timeStamp>
    inRdsFullName = os.path.basename( rdsPath )
    tmplst = inRdsFullName.split("_@_")
    return tmplst[1]

def getTestNameFromRdsPath(rdsPath): # last folder name sample: <testName>_@_<timeStamp>
    inRdsFullName = os.path.basename( rdsPath )
    tmplst = inRdsFullName.split("_@_")
    return tmplst[0]

def getInputVideoFile(rdsPath, filename_postfix=""): # retrievely searching video file in Rds path and return the first found
    tmpFileLst = FolderOp.getFileListWithKeyword(rdsPath, f"{filename_postfix}.mp4")
    if len(tmpFileLst)>0:        return os.path.join(rdsPath, tmpFileLst[0])
    tmpFileLst = FolderOp.getFileListWithKeyword(rdsPath, f"{filename_postfix}.MOV")
    if len(tmpFileLst)>0:        return os.path.join(rdsPath, tmpFileLst[0])
    tmpFolderList = FolderOp.getSubFolderListWithKeyword(rdsPath, "")
    if len(tmpFolderList)>0:
        tmpFolderPath = os.path.join(rdsPath, tmpFolderList[0])
        tmpFileLst = FolderOp.getFileListWithKeyword(tmpFolderPath, f"{filename_postfix}.mp4")
        if len(tmpFileLst)>0:            return os.path.join(tmpFolderPath, tmpFileLst[0])
        tmpFileLst = FolderOp.getFileListWithKeyword(tmpFolderPath, f"{filename_postfix}.MOV")
        if len(tmpFileLst)>0:            return os.path.join(tmpFolderPath, tmpFileLst[0])
    return ""
