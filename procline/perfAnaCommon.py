import os, importlib, cv2, numpy
from tools import anPerfToolOcr, JsonFileOp, anPerfToolFrameWarp, FolderOp

configDict = {}
dutCoreRect_pts = None
g_debug_level = 0
debugFrameIndexList = []
debugWorkPath = ""
videoFPS = 240
commonPreprocMethodObjList = []

def getFPS(videoFile):
    fps = -1
    cap = cv2.VideoCapture(videoFile)
    if cap.isOpened(): # Check if the video opened successfully
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the FPS property
        print(f"Frames per Second (FPS): {fps}")
    else:
        print("Error: Could not open the video file.")
    cap.release()  # Release the video object
    return fps

def init(videoFile, configPath, debugFrameIdxLst=[], debugPath=""):
    global configDict, debugFrameIndexList, debugWorkPath, g_debug_level, dutCoreRect_pts, videoFPS, commonPreprocMethodObjList
    videoFPS = getFPS(videoFile)
    if videoFPS<0:
        return -1
    if os.path.isdir(debugPath):
        debugFrameIndexList = debugFrameIdxLst
        debugWorkPath = debugPath
    # common config for video analysis system (OCR srv address, ...)
    configFile = os.path.join(configPath, "commonConfigDict.txt")
    configDict = JsonFileOp.loadDict(configFile)
    if 0==len(configDict):
        return -1
    g_debug_level = configDict["debug_level"]
    dutCoreRectConfigFile = os.path.join(configPath, "DutCoreRect.csv")
    if not os.path.exists(dutCoreRectConfigFile):
        print("Error: no DutCoreRect.csv not found!")
        return -1
    dutCoreRect_pts = numpy.loadtxt(dutCoreRectConfigFile, delimiter=',')
    ### 1. init basic tools before start compute line
    anPerfToolOcr.init( configDict["ocr_srv_url"] )
    ### 2. load common preproc methods
    if "commonPreprocMethodList" in configDict.keys():
        commonPreprocMethodObjList = selectPreProcMethodList( configDict["commonPreprocMethodList"] )
    return 0

def getCaseConfigDict(caseConfigPath, rdsTestName):
    configFile = os.path.join(caseConfigPath, rdsTestName+".configDict.txt")
    if not os.path.isfile(configFile):        configFile = os.path.join(caseConfigPath, rdsTestName+".conf")
    return JsonFileOp.loadDict( configFile ) # detailed config of the video analysis compute line

def preproc(frame):
    global dutCoreRect_pts, commonPreprocMethodObjList
    # crop core rect and wrap is solid first preprocessing
    ret = anPerfToolFrameWarp.proc(frame, dutCoreRect_pts)
    if len(commonPreprocMethodObjList)==0:
        return ret
    # do the other preprocessings
    for preprocObj in commonPreprocMethodObjList:
        ret = preprocObj.proc(ret, 0)
    return ret

def selectPreProcMethodList(preprocMethodNameList):
    if len(preprocMethodNameList)<=0:
        return []
    retlst = []
    for n in preprocMethodNameList:
        preprocObj = selectPreProcMethod(n)
        if preprocObj is None:
            print(f"Error: failed to find preproc method -- {n}")
            return []
        retlst.append(preprocObj)
    return retlst

def selectPreProcMethod(preprocMethodName):
    if len(preprocMethodName)>0:
        print(f"Info: load preprocess method -- {preprocMethodName}")
        return getClassObj( "method4preproc", preprocMethodName )
    return None

def getClassObj(methodLibName, moduleClassName):
    try:
        # 1. Dynamically import the module
        compModule = importlib.import_module( f"{methodLibName}.{moduleClassName}" )
        # 2. Get the class from the module
        cls = getattr(compModule, moduleClassName)
        # 3. new object (passing any required arguments)
        return cls() #cls(*args, **kwargs)
    except Exception as e:
        print(f"Error in getClassObj: {e}")
        return None
