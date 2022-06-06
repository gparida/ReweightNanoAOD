
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


WJets_HT_2500toInfConfig = ReweightConfiguration()
WJets_HT_2500toInfConfig.name = 'WJets_HT-2500toInf'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WJets_HT_2500toInfConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(WJets_HT_2500toInfConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WJets_HT_2500toInfConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WJets_HT_2500toInfConfig.inputFile = jsonInfo[WJets_HT_2500toInfConfig.name]['file']
WJets_HT_2500toInfConfig.inputFile_tt = jsonInfo[WJets_HT_2500toInfConfig.name]['file_tt']
WJets_HT_2500toInfConfig.inputFile_et = jsonInfo[WJets_HT_2500toInfConfig.name]['file_et']
WJets_HT_2500toInfConfig.inputFile_mt = jsonInfo[WJets_HT_2500toInfConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WJets_HT_2500toInfConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WJets_HT_2500toInfConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WJets_HT_2500toInfConfig.listOfWeights = list
