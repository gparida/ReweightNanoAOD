from Utilities.RecursiveLoader import RecursiveLoader
from Configurations.ConfigDefinition import ReweightConfiguration
import argparse
import traceback
import sys
import glob
import ROOT


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Handle script for performing final reweighting of events')
    	parser.add_argument('--ConfigFiles',nargs = '+',help="Python based config files used to specify samples",required=True)

    	args = parser.parse_args()
    	theLoader= RecursiveLoader()
	for configFile in args.ConfigFiles:
		print("Loading from configFile: "+configFile)
		theConfigModule = theLoader.LoadFromDirectoryPath(configFile)	
	
