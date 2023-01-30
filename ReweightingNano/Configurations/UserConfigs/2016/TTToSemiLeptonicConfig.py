
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


TTToSemiLeptonicConfig = ReweightConfiguration()
TTToSemiLeptonicConfig.name = 'TTToSemiLeptonic'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
TTToSemiLeptonicConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(TTToSemiLeptonicConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[TTToSemiLeptonicConfig.name]['file'])
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

TTToSemiLeptonicConfig.inputFile = jsonInfo[TTToSemiLeptonicConfig.name]['file']
#TTToSemiLeptonicConfig.inputFile_tt = jsonInfo[TTToSemiLeptonicConfig.name]['file_tt']
#TTToSemiLeptonicConfig.inputFile_et = jsonInfo[TTToSemiLeptonicConfig.name]['file_et']
#TTToSemiLeptonicConfig.inputFile_mt = jsonInfo[TTToSemiLeptonicConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[TTToSemiLeptonicConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[TTToSemiLeptonicConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


TTToSemiLeptonicConfig.listOfWeights = list
