import ROOT
import os
import json

from Configurations.ConfigDefinition import ReweightConfiguration

DataConfig = ReweightConfiguration()
DataConfig.name = 'Data'
#DataConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DataConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(DataConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DataConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DataConfig.inputFile = jsonInfo[DataConfig.name]['file']
DataConfig.inputFile_tt = jsonInfo[DataConfig.name]['file_tt']
DataConfig.inputFile_et = jsonInfo[DataConfig.name]['file_et']
DataConfig.inputFile_mt = jsonInfo[DataConfig.name]['file_mt']


DataConfig.listOfWeights = [
]
