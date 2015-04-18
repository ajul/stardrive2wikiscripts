import xml.etree.ElementTree as ElementTree
import os

def iterDirXML(dirname):
    """Given a directory, iterate over the content of the .txt files in that directory as Trees"""
    for filename in os.listdir(dirname):
        fullpath = os.path.join(dirname, filename)
        if os.path.isfile(fullpath):
            _, ext = os.path.splitext(fullpath)
            if ext == ".xml":
                yield filename, ElementTree.parse(fullpath)
