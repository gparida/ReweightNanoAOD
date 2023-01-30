
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


WJetsToLNu_HT_1200To2500Config = ReweightConfiguration()
WJetsToLNu_HT_1200To2500Config.name = 'WJetsToLNu_HT-1200To2500'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
WJetsToLNu_HT_1200To2500Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(WJetsToLNu_HT_1200To2500Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WJetsToLNu_HT_1200To2500Config.inputFile = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['file']
#WJetsToLNu_HT_1200To2500Config.inputFile_tt = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['file_tt']
#WJetsToLNu_HT_1200To2500Config.inputFile_et = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['file_et']
#WJetsToLNu_HT_1200To2500Config.inputFile_mt = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WJetsToLNu_HT_1200To2500Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WJetsToLNu_HT_1200To2500Config.listOfWeights = list
