
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WWTo1L1Nu2Q_4fConfig = ReweightConfiguration()
WWTo1L1Nu2Q_4fConfig.name = 'WWTo1L1Nu2Q_4f'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WWTo1L1Nu2Q_4fConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(WWTo1L1Nu2Q_4fConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['file'])
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

WWTo1L1Nu2Q_4fConfig.inputFile = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['file']
#WWTo1L1Nu2Q_4fConfig.inputFile_tt = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['file_tt']
#WWTo1L1Nu2Q_4fConfig.inputFile_et = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['file_et']
#WWTo1L1Nu2Q_4fConfig.inputFile_mt = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WWTo1L1Nu2Q_4fConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WWTo1L1Nu2Q_4fConfig.listOfWeights = list
