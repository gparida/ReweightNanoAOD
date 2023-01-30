
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WZTo1L1Nu2Q_4fConfig = ReweightConfiguration()
WZTo1L1Nu2Q_4fConfig.name = 'WZTo1L1Nu2Q_4f'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WZTo1L1Nu2Q_4fConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(WZTo1L1Nu2Q_4fConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['file'])
runTree = theFile.Get('Runs')
nEntries = runTree.GetEntries()
totalNumberOfEvents = 0.0
for x in range(nEntries):
    runTree.GetEntry(x)
    #print ("The sum of gen weight of a single file = ",runTree.genEventSumw)
    totalNumberOfEvents += runTree.genEventSumw

print ("Final sum of weights = ",totalNumberOfEvents)

#totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WZTo1L1Nu2Q_4fConfig.inputFile = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['file']
#WZTo1L1Nu2Q_4fConfig.inputFile_tt = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['file_tt']
#WZTo1L1Nu2Q_4fConfig.inputFile_et = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['file_et']
#WZTo1L1Nu2Q_4fConfig.inputFile_mt = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WZTo1L1Nu2Q_4fConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WZTo1L1Nu2Q_4fConfig.listOfWeights = list
