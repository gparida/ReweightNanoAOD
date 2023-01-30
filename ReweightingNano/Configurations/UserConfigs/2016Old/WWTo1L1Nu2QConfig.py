
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WWTo1L1Nu2QConfig = ReweightConfiguration()
WWTo1L1Nu2QConfig.name = 'WWTo1L1Nu2Q'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WWTo1L1Nu2QConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(WWTo1L1Nu2QConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WWTo1L1Nu2QConfig.name]['file'])
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

WWTo1L1Nu2QConfig.inputFile = jsonInfo[WWTo1L1Nu2QConfig.name]['file']
#WWTo1L1Nu2QConfig.inputFile_tt = jsonInfo[WWTo1L1Nu2QConfig.name]['file_tt']
#WWTo1L1Nu2QConfig.inputFile_et = jsonInfo[WWTo1L1Nu2QConfig.name]['file_et']
#WWTo1L1Nu2QConfig.inputFile_mt = jsonInfo[WWTo1L1Nu2QConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WWTo1L1Nu2QConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WWTo1L1Nu2QConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WWTo1L1Nu2QConfig.listOfWeights = list
