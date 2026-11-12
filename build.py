import os, sys, shutil, time

def _rmFolders(workPath, FolderNameList):
    for fd in FolderNameList:
        rmpath = os.path.join(workPath, fd)
        if os.path.isdir(rmpath):            shutil.rmtree( rmpath )

def find_and_replace(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        file_content = file.read()
    # 2. Replace all occurrences of the target string
    new_content = file_content.replace(old_text, new_text)
    # 3. Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

def insert_multiline_at(file_path, line_number, new_content):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # 2. Insert new content at the specified line (0-indexed)
    if not new_content.endswith('\n'):
        new_content += '\n'
    lines.insert(line_number - 1, new_content)
    # 3. Write everything back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)


if __name__ == "__main__":
    insertCodeString = """import os, sys
from PyInstaller.utils.hooks import collect_submodules

sys.path.append(os.path.abspath(os.getcwd()))

hidden_modules = []
hidden_modules += collect_submodules('method4preproc')
hidden_modules += collect_submodules('method4proc')
"""
    t1 = time.time()
    srcWorkPath = os.getcwd()    #codeProjectName = os.path.basename(srcWorkPath)
    _rmFolders(srcWorkPath, ["build", "dist"]) # clear build folders in src code path
    os.system(f"pyi-makespec --onefile anperf.py") # build anperf.spec file
    time.sleep(1)
    find_and_replace('anperf.spec', "hiddenimports=[]", "hiddenimports=hidden_modules")
    insert_multiline_at('anperf.spec', 2, insertCodeString)
    time.sleep(1)
    os.system(f"pyinstaller anperf.spec")
    t2 = time.time()
    print("build done in " + str(t2-t1))
