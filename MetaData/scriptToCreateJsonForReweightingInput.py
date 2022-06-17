#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser(description='A script to create the skeleton of the samples JSON file which has the dataset name key. It also has the path to the file and keys for XS and Kfactor lumi etc')
parser.add_argument('-b', '--basePath',help="Enter base path of Location of Root Files",required=True)
#parser.add_argument('--haddDir',help="Folder in which the files are present",required=True)
#parser.add_argument('--savePath',help="Place where to store the hadded files",required=True)
args = parser.parse_args()



base_path = Path(args.basePath)
#searchPhrase = "_13TeV"
finalDict = dict()
keyname=[files.name[-5:] for files in list(base_path.glob("*.root"))]
print (keyname)

{x:dict() for x in keyname}

for key in keyname:
    print (key, type((key)))










#f = open("fileList.json", "a")
#f.write('{'+'\n')

#for files in list(base_path.glob("*.root")):
#    keyname = files.name[-5:]
#
#
#    if not campaigns.is_dir():
#        continue
#
#    dataset_path = Path(args.basePath+"/"+campaigns.name+"/")
#    for dataset in dataset_path.iterdir():
#        if not dataset.is_dir():
#            continue
#
#        if searchPhrase in dataset.name:
#            print (f"{dataset.name} has  "+searchPhrase+" in it")
#            #print(dataset.name+" has "+searchPhrase+" in it ")
#        keyname = f'{dataset.name[:dataset.name.index(searchPhrase)]}'
#        listDict[keyname]=args.basePath+'/'+campaigns.name+'/'+dataset.name+'/*.root'
#        #keyname = dataset.name[:dataset.name.index(searchPhrase)]
#        #f.write('\t'+'"'+keyname+'":"'+args.basePath+'/'+campaigns.name+'/'+dataset.name+'/*.root'+'",'+'\n')
#
##result = json.dumps(listDict, indent = 4, sort_keys = True)
##print (result)
#with open("fileList.json", 'w') as writeFile:
#        json.dump(listDict, writeFile, indent=4)