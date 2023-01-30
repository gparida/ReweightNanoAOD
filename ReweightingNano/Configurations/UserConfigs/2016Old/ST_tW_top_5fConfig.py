
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ST_tW_top_5fConfig = ReweightConfiguration()
ST_tW_top_5fConfig.name = 'ST_tW_top_5f'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ST_tW_top_5fConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SamplesJson_Old/2016_Samples.json'

with open(ST_tW_top_5fConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ST_tW_top_5fConfig.name]['file'])
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

ST_tW_top_5fConfig.inputFile = jsonInfo[ST_tW_top_5fConfig.name]['file']
#ST_tW_top_5fConfig.inputFile_tt = jsonInfo[ST_tW_top_5fConfig.name]['file_tt']
#ST_tW_top_5fConfig.inputFile_et = jsonInfo[ST_tW_top_5fConfig.name]['file_et']
#ST_tW_top_5fConfig.inputFile_mt = jsonInfo[ST_tW_top_5fConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ST_tW_top_5fConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ST_tW_top_5fConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ST_tW_top_5fConfig.listOfWeights = list
