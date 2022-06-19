#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import os


parser = argparse.ArgumentParser(description='Script to store the path to all the user configs for a specifc year and create a defaulConfigPass')
parser.add_argument('-y','--year',help="so that we know which year folder we need to put the configs")
args = parser.parse_args()

config_path = Path("Configurations/UserConfigs/"+args.year+"/")
config_dict = dict()

#config_names=["Configurations/UserConfigs/"+args.year+"/"+files.name[:] for files in list(config_path.glob("*Config*.py"))]

config_names=[files.as_posix() for files in list(config_path.glob("*Config*.py"))]

print (config_names)