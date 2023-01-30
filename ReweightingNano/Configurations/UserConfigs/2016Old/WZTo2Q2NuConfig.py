
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WZTo2Q2NuConfig = ReweightConfiguration()
WZTo2Q2NuConfig.name = 'WZTo2Q2Nu'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WZTo2Q2NuConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(WZTo2Q2NuConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WZTo2Q2NuConfig.name]['file'])
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

WZTo2Q2NuConfig.inputFile = jsonInfo[WZTo2Q2NuConfig.name]['file']
#WZTo2Q2NuConfig.inputFile_tt = jsonInfo[WZTo2Q2NuConfig.name]['file_tt']
#WZTo2Q2NuConfig.inputFile_et = jsonInfo[WZTo2Q2NuConfig.name]['file_et']
#WZTo2Q2NuConfig.inputFile_mt = jsonInfo[WZTo2Q2NuConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WZTo2Q2NuConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WZTo2Q2NuConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WZTo2Q2NuConfig.listOfWeights = list
