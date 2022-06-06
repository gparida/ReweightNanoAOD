import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

WZConfig = ReweightConfiguration()
WZConfig.name = 'WZ'
#WZConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WZConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(WZConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WZConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WZConfig.inputFile = jsonInfo[WZConfig.name]['file']
WZConfig.inputFile_tt = jsonInfo[WZConfig.name]['file_tt']
WZConfig.inputFile_et = jsonInfo[WZConfig.name]['file_et']
WZConfig.inputFile_mt = jsonInfo[WZConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WZConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WZConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WZConfig.listOfWeights = list
