
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


DYJetsToLL_M_50_HT_800to1200Config = ReweightConfiguration()
DYJetsToLL_M_50_HT_800to1200Config.name = 'DYJetsToLL_M-50_HT-800to1200'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYJetsToLL_M_50_HT_800to1200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(DYJetsToLL_M_50_HT_800to1200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['file'])
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

DYJetsToLL_M_50_HT_800to1200Config.inputFile = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['file']
#DYJetsToLL_M_50_HT_800to1200Config.inputFile_tt = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['file_tt']
#DYJetsToLL_M_50_HT_800to1200Config.inputFile_et = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['file_et']
#DYJetsToLL_M_50_HT_800to1200Config.inputFile_mt = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYJetsToLL_M_50_HT_800to1200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYJetsToLL_M_50_HT_800to1200Config.listOfWeights = list
