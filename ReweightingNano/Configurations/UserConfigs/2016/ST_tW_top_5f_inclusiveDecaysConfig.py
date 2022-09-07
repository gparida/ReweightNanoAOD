
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ST_tW_top_5f_inclusiveDecaysConfig = ReweightConfiguration()
ST_tW_top_5f_inclusiveDecaysConfig.name = 'ST_tW_top_5f_inclusiveDecays'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ST_tW_top_5f_inclusiveDecaysConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ST_tW_top_5f_inclusiveDecaysConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ST_tW_top_5f_inclusiveDecaysConfig.inputFile = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['file']
#ST_tW_top_5f_inclusiveDecaysConfig.inputFile_tt = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['file_tt']
#ST_tW_top_5f_inclusiveDecaysConfig.inputFile_et = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['file_et']
#ST_tW_top_5f_inclusiveDecaysConfig.inputFile_mt = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ST_tW_top_5f_inclusiveDecaysConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ST_tW_top_5f_inclusiveDecaysConfig.listOfWeights = list
