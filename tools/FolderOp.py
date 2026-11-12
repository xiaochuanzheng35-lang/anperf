import os, json, shutil

def mkSubFdinSpecPath( specpath, subfdname ):
    fdpath = os.path.join( specpath, subfdname )
    if not os.path.isdir(fdpath):
        os.mkdir(fdpath)
    return fdpath

def getSubFolderListWithKeyword( specpath, keyword ):
    retList = []
    for df in os.listdir(specpath):
        if (keyword in df) and (os.path.isdir(os.path.join(specpath, df))):
            retList.append( df )
    return retList

def getFileListWithKeyword( specpath, keyword ):
    retList = []
    for df in os.listdir(specpath):
        if (keyword in df) and (os.path.isfile(os.path.join(specpath, df))):
            retList.append( df )
    return retList

def copyFileListToDestPath( filelist, specpath ):
    for f in filelist:
        dstfile = os.path.join( specpath, os.path.basename(f) )
        shutil.copy(f, dstfile)

def purgeSpecPath( specpath ):
    print("Purging path : " + specpath)
    for fd in os.listdir(specpath):
        file_path = os.path.join(specpath, fd)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)                #print(f"Deleted {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)                #print(f"Deleted directory {file_path}")
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def deleteAllFileWithSpecExtension(specpath, specFileExtension):
    for fd in os.listdir(specpath):
        file_path = os.path.join(specpath, fd)
        try:
            if os.path.isfile(file_path) and file_path.endswith(specFileExtension):
                os.remove(file_path)                #print(f"Deleted {file_path}")
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
