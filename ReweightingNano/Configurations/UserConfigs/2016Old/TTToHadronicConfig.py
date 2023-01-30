
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


TTToHadronicConfig = ReweightConfiguration()
TTToHadronicConfig.name = 'TTToHadronic'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
TTToHadronicConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(TTToHadronicConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[TTToHadronicConfig.name]['file'])
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

TTToHadronicConfig.inputFile = jsonInfo[TTToHadronicConfig.name]['file']
#TTToHadronicConfig.inputFile_tt = jsonInfo[TTToHadronicConfig.name]['file_tt']
#TTToHadronicConfig.inputFile_et = jsonInfo[TTToHadronicConfig.name]['file_et']
#TTToHadronicConfig.inputFile_mt = jsonInfo[TTToHadronicConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[TTToHadronicConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[TTToHadronicConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


TTToHadronicConfig.listOfWeights = list
