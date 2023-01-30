
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ZZTo2Nu2Q_5fConfig = ReweightConfiguration()
ZZTo2Nu2Q_5fConfig.name = 'ZZTo2Nu2Q_5f'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ZZTo2Nu2Q_5fConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ZZTo2Nu2Q_5fConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ZZTo2Nu2Q_5fConfig.name]['file'])
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

ZZTo2Nu2Q_5fConfig.inputFile = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['file']
#ZZTo2Nu2Q_5fConfig.inputFile_tt = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['file_tt']
#ZZTo2Nu2Q_5fConfig.inputFile_et = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['file_et']
#ZZTo2Nu2Q_5fConfig.inputFile_mt = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ZZTo2Nu2Q_5fConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ZZTo2Nu2Q_5fConfig.listOfWeights = list
