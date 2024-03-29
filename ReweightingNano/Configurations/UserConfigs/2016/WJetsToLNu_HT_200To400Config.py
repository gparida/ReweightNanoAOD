
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WJetsToLNu_HT_200To400Config = ReweightConfiguration()
WJetsToLNu_HT_200To400Config.name = 'WJetsToLNu_HT-200To400'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WJetsToLNu_HT_200To400Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(WJetsToLNu_HT_200To400Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WJetsToLNu_HT_200To400Config.name]['file'])
runTree = theFile.Get('Runs')
nEntries = runTree.GetEntries()
totalNumberOfEvents_runTree = 0.0
for x in range(nEntries):
    runTree.GetEntry(x)
    #print ("The sum of gen weight of a single file = ",runTree.genEventSumw)
    totalNumberOfEvents_runTree += runTree.genEventSumw

print ("Sum of weights from run tree = ",totalNumberOfEvents_runTree)

#totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
totalNumberOfEvents = totalNumberOfEvents_runTree

print ("Sum of weights from histogram = ",theFile.cutflow.GetBinContent(1))
print ("The one we will use = ",totalNumberOfEvents)
theFile.Close()

WJetsToLNu_HT_200To400Config.inputFile = jsonInfo[WJetsToLNu_HT_200To400Config.name]['file']
#WJetsToLNu_HT_200To400Config.inputFile_tt = jsonInfo[WJetsToLNu_HT_200To400Config.name]['file_tt']
#WJetsToLNu_HT_200To400Config.inputFile_et = jsonInfo[WJetsToLNu_HT_200To400Config.name]['file_et']
#WJetsToLNu_HT_200To400Config.inputFile_mt = jsonInfo[WJetsToLNu_HT_200To400Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WJetsToLNu_HT_200To400Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WJetsToLNu_HT_200To400Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WJetsToLNu_HT_200To400Config.listOfWeights = list
