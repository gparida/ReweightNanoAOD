
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ST_t_channel_top_4f_InclusiveDecaysConfig = ReweightConfiguration()
ST_t_channel_top_4f_InclusiveDecaysConfig.name = 'ST_t-channel_top_4f_InclusiveDecays'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ST_t_channel_top_4f_InclusiveDecaysConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ST_t_channel_top_4f_InclusiveDecaysConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['file'])
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

ST_t_channel_top_4f_InclusiveDecaysConfig.inputFile = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['file']
#ST_t_channel_top_4f_InclusiveDecaysConfig.inputFile_tt = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['file_tt']
#ST_t_channel_top_4f_InclusiveDecaysConfig.inputFile_et = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['file_et']
#ST_t_channel_top_4f_InclusiveDecaysConfig.inputFile_mt = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ST_t_channel_top_4f_InclusiveDecaysConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ST_t_channel_top_4f_InclusiveDecaysConfig.listOfWeights = list
