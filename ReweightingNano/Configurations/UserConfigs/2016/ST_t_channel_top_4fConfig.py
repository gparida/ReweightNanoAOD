
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ST_t_channel_top_4fConfig = ReweightConfiguration()
ST_t_channel_top_4fConfig.name = 'ST_t-channel_top_4f'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ST_t_channel_top_4fConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(ST_t_channel_top_4fConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ST_t_channel_top_4fConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ST_t_channel_top_4fConfig.inputFile = jsonInfo[ST_t_channel_top_4fConfig.name]['file']
ST_t_channel_top_4fConfig.inputFile_tt = jsonInfo[ST_t_channel_top_4fConfig.name]['file_tt']
ST_t_channel_top_4fConfig.inputFile_et = jsonInfo[ST_t_channel_top_4fConfig.name]['file_et']
ST_t_channel_top_4fConfig.inputFile_mt = jsonInfo[ST_t_channel_top_4fConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ST_t_channel_top_4fConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ST_t_channel_top_4fConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ST_t_channel_top_4fConfig.listOfWeights = list
