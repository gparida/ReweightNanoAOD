
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ZZTo2Q2L_mllmin4p0Config = ReweightConfiguration()
ZZTo2Q2L_mllmin4p0Config.name = 'ZZTo2Q2L_mllmin4p0'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ZZTo2Q2L_mllmin4p0Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ZZTo2Q2L_mllmin4p0Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['file'])
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

ZZTo2Q2L_mllmin4p0Config.inputFile = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['file']
#ZZTo2Q2L_mllmin4p0Config.inputFile_tt = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['file_tt']
#ZZTo2Q2L_mllmin4p0Config.inputFile_et = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['file_et']
#ZZTo2Q2L_mllmin4p0Config.inputFile_mt = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ZZTo2Q2L_mllmin4p0Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ZZTo2Q2L_mllmin4p0Config.listOfWeights = list
