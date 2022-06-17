#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser(description='A script to create the skeleton of the samples JSON file which has the dataset name key. It also has the path to the file and keys for XS and Kfactor lumi etc')
parser.add_argument('-b', '--basePath',help="Enter base path of Location of Root Files",required=True)
parser.add_argument('-s','--savePath',help="where to dump the json file along with the name")
#parser.add_argument('--haddDir',help="Folder in which the files are present",required=True)
#parser.add_argument('--savePath',help="Place where to store the hadded files",required=True)
args = parser.parse_args()



base_path = Path(args.basePath)
#searchPhrase = "_13TeV"
finalDict = dict()
keyname=[files.name[:-5] for files in list(base_path.glob("*.root"))]
print (keyname)

{x:dict() for x in keyname}

for key in keyname:
    filePath = args.basePath + "/" + key + ".root"
    finalDict[key] = {"file":filePath, "XS": 0, "kFac": 0, "EquiLumi":0}


print (finalDict)

with open(args.savePath, 'w') as writeFile:
        json.dump(finalDict, writeFile, indent=4)


































