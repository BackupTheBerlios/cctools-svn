import os
import fnmatch

def findZcml(basePath):
    """Walk the working directory for ZCML files which will be installed
    alongside the byte-code files."""

    IGNORE_DIRS = ('dist', 'build', 'extensions')
    
    result = []

    # walk the directory tree, ignoring distutils folders
    for (dirpath, dirnames, filenames) in os.walk(basePath, topdown=True):

        # prune out any distutils folders in subpaths
        for ign in IGNORE_DIRS:
            if ign in dirnames: dirnames.remove(ign)

        # strip out the common portion of the path
        relpath = dirpath[len(basePath)+1:]

        # filter out only ZCML files
        zcml = fnmatch.filter(filenames, "*.zcml")
        
        if len(zcml) > 0:
            result.append((relpath, [os.path.join(relpath, n) for n in zcml]))

    return result

def packageData(pkgList):
    result = {}

    for package in pkgList:
        result[package] = ['*.zcml']

    return result

def locale_files(base_dir):
    
    result = []

    # walk the directory tree, ignoring distutils folders
    for (dirpath, dirnames, filenames) in os.walk(base_dir, topdown=True):

        # strip out the common portion of the path
        relpath = dirpath[len(base_dir)+1:]

        # filter out only locale files
        zcml = fnmatch.filter(filenames, "*.[pm]o") + \
               fnmatch.filter(filenames, "*.pot") 
        
        if len(zcml) > 0:
            result.append((relpath, [os.path.join(relpath, n) for n in zcml]))

    return result
