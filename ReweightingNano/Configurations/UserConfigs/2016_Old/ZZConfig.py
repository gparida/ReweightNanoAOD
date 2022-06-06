import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

ZZConfig = ReweightConfiguration()
ZZConfig.name = 'ZZ'
#ZZConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ZZConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(ZZConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ZZConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ZZConfig.inputFile = jsonInfo[ZZConfig.name]['file']
ZZConfig.inputFile_tt = jsonInfo[ZZConfig.name]['file_tt']
ZZConfig.inputFile_et = jsonInfo[ZZConfig.name]['file_et']
ZZConfig.inputFile_mt = jsonInfo[ZZConfig.name]['file_mt']

crossSectionWeight.XS = jsonInfo[ZZConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ZZConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ZZConfig.listOfWeights = list
