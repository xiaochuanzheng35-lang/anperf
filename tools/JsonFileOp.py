import os, json


def dumpDict( inputDict, specfile ):
    if len(specfile)>0:
        with open( specfile, 'w', encoding="utf-8" ) as f:
            json.dump(inputDict, f, indent=4, ensure_ascii=False)
    return 0

def dumpDictSimple( inputDict, specfile ):
    if len(specfile)>0:
        with open( specfile, 'w', encoding="utf-8" ) as f:
            json.dump(inputDict, f)
    return 0

def loadDict( dictfile ):
    retDict = {}
    if os.path.isfile(dictfile):
        with open(dictfile, 'r', encoding="utf-8") as file:
            retDict = json.load(file)            #print(retDict)
    return retDict
