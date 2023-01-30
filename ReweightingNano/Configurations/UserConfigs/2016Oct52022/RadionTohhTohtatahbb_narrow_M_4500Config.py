
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


RadionTohhTohtatahbb_narrow_M_4500Config = ReweightConfiguration()
RadionTohhTohtatahbb_narrow_M_4500Config.name = 'RadionTohhTohtatahbb_narrow_M-4500'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
RadionTohhTohtatahbb_narrow_M_4500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(RadionTohhTohtatahbb_narrow_M_4500Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['file'])
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

RadionTohhTohtatahbb_narrow_M_4500Config.inputFile = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['file']
#RadionTohhTohtatahbb_narrow_M_4500Config.inputFile_tt = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['file_tt']
#RadionTohhTohtatahbb_narrow_M_4500Config.inputFile_et = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['file_et']
#RadionTohhTohtatahbb_narrow_M_4500Config.inputFile_mt = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[RadionTohhTohtatahbb_narrow_M_4500Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


RadionTohhTohtatahbb_narrow_M_4500Config.listOfWeights = list
