
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


RadionTohhTohtatahbb_narrow_M_1800Config = ReweightConfiguration()
RadionTohhTohtatahbb_narrow_M_1800Config.name = 'RadionTohhTohtatahbb_narrow_M-1800'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
RadionTohhTohtatahbb_narrow_M_1800Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(RadionTohhTohtatahbb_narrow_M_1800Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['file'])
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

RadionTohhTohtatahbb_narrow_M_1800Config.inputFile = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['file']
#RadionTohhTohtatahbb_narrow_M_1800Config.inputFile_tt = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['file_tt']
#RadionTohhTohtatahbb_narrow_M_1800Config.inputFile_et = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['file_et']
#RadionTohhTohtatahbb_narrow_M_1800Config.inputFile_mt = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[RadionTohhTohtatahbb_narrow_M_1800Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


RadionTohhTohtatahbb_narrow_M_1800Config.listOfWeights = list
