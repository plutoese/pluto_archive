# coding=UTF-8

import os

# A class to deal with file system
class FileSystem:
    # Constructor
    def __init__(self,path,file=None):
        self.path = path
        if file is not None:
            self.file = file

    # list files in a path
    def listdir(self):
        return os.listdir(self.path)

    # list files in a path with absolute path
    def listabsdir(self):
        files = []
        for item in self.listdir():
            if os.path.isdir(os.path.join(self.path,item)):
                files.append({item:[os.path.join(os.path.join(self.path,item),file) for file in os.listdir(os.path.join(self.path,item))]})
            else:
                files.append(os.path.join(self.path,item))
        return files

    # list allfiles in a path with relative path
    def listallfiles(self):
        files = []
        for item in self.listdir():
            mpath = os.path.join(self.path,item)
            if os.path.isdir(mpath):
                files.extend(FileSystem(mpath).listallfiles())
            else:
                files.append(mpath)
        return files


if __name__ == '__main__':
    path = r'C:\Data\acode'
    mos = FileSystem(path)
    files = mos.listabsdir()
    print(files)

