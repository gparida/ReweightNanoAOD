
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


DYJets_HT_800to1200Config = ReweightConfiguration()
DYJets_HT_800to1200Config.name = 'DYJets_HT-800to1200'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYJets_HT_800to1200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(DYJets_HT_800to1200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYJets_HT_800to1200Config.name]['file'])
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

DYJets_HT_800to1200Config.inputFile = jsonInfo[DYJets_HT_800to1200Config.name]['file']
#DYJets_HT_800to1200Config.inputFile_tt = jsonInfo[DYJets_HT_800to1200Config.name]['file_tt']
#DYJets_HT_800to1200Config.inputFile_et = jsonInfo[DYJets_HT_800to1200Config.name]['file_et']
#DYJets_HT_800to1200Config.inputFile_mt = jsonInfo[DYJets_HT_800to1200Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYJets_HT_800to1200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYJets_HT_800to1200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYJets_HT_800to1200Config.listOfWeights = list
