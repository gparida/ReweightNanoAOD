
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WZTo1L1nu2qConfig = ReweightConfiguration()
WZTo1L1nu2qConfig.name = 'WZTo1L1nu2q'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WZTo1L1nu2qConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(WZTo1L1nu2qConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WZTo1L1nu2qConfig.name]['file'])
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

WZTo1L1nu2qConfig.inputFile = jsonInfo[WZTo1L1nu2qConfig.name]['file']
#WZTo1L1nu2qConfig.inputFile_tt = jsonInfo[WZTo1L1nu2qConfig.name]['file_tt']
#WZTo1L1nu2qConfig.inputFile_et = jsonInfo[WZTo1L1nu2qConfig.name]['file_et']
#WZTo1L1nu2qConfig.inputFile_mt = jsonInfo[WZTo1L1nu2qConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WZTo1L1nu2qConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WZTo1L1nu2qConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WZTo1L1nu2qConfig.listOfWeights = list
