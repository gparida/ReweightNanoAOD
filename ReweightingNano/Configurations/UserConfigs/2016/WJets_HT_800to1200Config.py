
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WJets_HT_800to1200Config = ReweightConfiguration()
WJets_HT_800to1200Config.name = 'WJets_HT-800to1200'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WJets_HT_800to1200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(WJets_HT_800to1200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WJets_HT_800to1200Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WJets_HT_800to1200Config.inputFile = jsonInfo[WJets_HT_800to1200Config.name]['file']
WJets_HT_800to1200Config.inputFile_tt = jsonInfo[WJets_HT_800to1200Config.name]['file_tt']
WJets_HT_800to1200Config.inputFile_et = jsonInfo[WJets_HT_800to1200Config.name]['file_et']
WJets_HT_800to1200Config.inputFile_mt = jsonInfo[WJets_HT_800to1200Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WJets_HT_800to1200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WJets_HT_800to1200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WJets_HT_800to1200Config.listOfWeights = list
