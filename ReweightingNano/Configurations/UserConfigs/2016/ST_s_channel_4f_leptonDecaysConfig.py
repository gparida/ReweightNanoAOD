
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ST_s_channel_4f_leptonDecaysConfig = ReweightConfiguration()
ST_s_channel_4f_leptonDecaysConfig.name = 'ST_s-channel_4f_leptonDecays'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ST_s_channel_4f_leptonDecaysConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ST_s_channel_4f_leptonDecaysConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ST_s_channel_4f_leptonDecaysConfig.inputFile = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['file']
#ST_s_channel_4f_leptonDecaysConfig.inputFile_tt = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['file_tt']
#ST_s_channel_4f_leptonDecaysConfig.inputFile_et = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['file_et']
#ST_s_channel_4f_leptonDecaysConfig.inputFile_mt = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ST_s_channel_4f_leptonDecaysConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ST_s_channel_4f_leptonDecaysConfig.listOfWeights = list
