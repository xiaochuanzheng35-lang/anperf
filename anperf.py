import os, sys
from tools import FolderOp, JsonFileOp
from procline import perfAnaMain, perfAnaCommon, testSources

if __name__ == "__main__":
    if 4==len(sys.argv) or 5==len(sys.argv):
        caseConfigPath   = sys.argv[1]
        inputProcRdsPath = sys.argv[2]
        outAnaDataPath   = sys.argv[3]
        debugWorkPath = ""
        debugFrameIdxList = []
        debugFrameIndexFile = ""
        ##### load debug frame index list and debug work path
        if 5==len(sys.argv):
            debugWorkPath = sys.argv[4]
            debugFrameIndexFile = os.path.join(debugWorkPath, "debugData.json")
            debugDataDict = JsonFileOp.loadDict(debugFrameIndexFile)        #print(debugDataDict)
            debugFrameIdxList = debugDataDict["keyFrameIndexList"]
        #####
        inRdsTestName = testSources.getTestNameFromRdsPath( inputProcRdsPath )
        print(f"process RdsTestName={inRdsTestName}")
        videoFile = testSources.getInputVideoFile( inputProcRdsPath )
        if 0==perfAnaCommon.init(videoFile, caseConfigPath, debugFrameIdxList, debugWorkPath): # load common configurations in spec path for whole process
            perfConfigDict = perfAnaCommon.getCaseConfigDict(caseConfigPath, inRdsTestName)
            # start the main analysis
            perfTimeDataDict = perfAnaMain.videoAnalyze(videoFile, perfConfigDict)
            # dump the analysis result
            if len(perfTimeDataDict)>0:
                perftimeInMS = int( float(perfTimeDataDict["perftime"]) * 1000 )
                testResDict = { "perftime"     : perftimeInMS }
                print(testResDict)
                testInfoDic = { "timeStampLst" : perfTimeDataDict["timeStampLst"] }
                print(testInfoDic)
                if os.path.isdir(outAnaDataPath):
                    JsonFileOp.dumpDict( testResDict, os.path.join(outAnaDataPath, "testResult.json") )
                    JsonFileOp.dumpDict( testInfoDic, os.path.join(outAnaDataPath, "testInfo.json") )
            ##### dump debug frame index list in debug work path
            JsonFileOp.dumpDictSimple( { "keyFrameIndexList" : perfAnaCommon.debugFrameIndexList }, debugFrameIndexFile )
            print(perfAnaCommon.debugFrameIndexList)
    else:
        print("Usage: python anperf.py  <ConfigPath>  <inputRdsPath>  <outputRdsPath>")
        print("or:    python anperf.py  <ConfigPath>  <inputRdsPath>  <outputRdsPath>  <debugWorkPath>")
