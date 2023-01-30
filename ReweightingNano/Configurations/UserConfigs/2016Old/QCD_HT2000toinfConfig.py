
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


QCD_HT2000toinfConfig = ReweightConfiguration()
QCD_HT2000toinfConfig.name = 'QCD_HT2000toinf'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
QCD_HT2000toinfConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(QCD_HT2000toinfConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_HT2000toinfConfig.name]['file'])
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

QCD_HT2000toinfConfig.inputFile = jsonInfo[QCD_HT2000toinfConfig.name]['file']
#QCD_HT2000toinfConfig.inputFile_tt = jsonInfo[QCD_HT2000toinfConfig.name]['file_tt']
#QCD_HT2000toinfConfig.inputFile_et = jsonInfo[QCD_HT2000toinfConfig.name]['file_et']
#QCD_HT2000toinfConfig.inputFile_mt = jsonInfo[QCD_HT2000toinfConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[QCD_HT2000toinfConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_HT2000toinfConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_HT2000toinfConfig.listOfWeights = list
