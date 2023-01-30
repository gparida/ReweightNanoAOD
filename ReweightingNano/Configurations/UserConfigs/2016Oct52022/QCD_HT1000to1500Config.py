
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


QCD_HT1000to1500Config = ReweightConfiguration()
QCD_HT1000to1500Config.name = 'QCD_HT1000to1500'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
QCD_HT1000to1500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(QCD_HT1000to1500Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_HT1000to1500Config.name]['file'])
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

QCD_HT1000to1500Config.inputFile = jsonInfo[QCD_HT1000to1500Config.name]['file']
#QCD_HT1000to1500Config.inputFile_tt = jsonInfo[QCD_HT1000to1500Config.name]['file_tt']
#QCD_HT1000to1500Config.inputFile_et = jsonInfo[QCD_HT1000to1500Config.name]['file_et']
#QCD_HT1000to1500Config.inputFile_mt = jsonInfo[QCD_HT1000to1500Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[QCD_HT1000to1500Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_HT1000to1500Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_HT1000to1500Config.listOfWeights = list
