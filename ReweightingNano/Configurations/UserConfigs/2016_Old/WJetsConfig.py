import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

WJetsConfig = ReweightConfiguration()
WJetsConfig.name = 'WJets'
#WJetsConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
WJetsConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(WJetsConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WJetsConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WJetsConfig.inputFile = jsonInfo[WJetsConfig.name]['file']
WJetsConfig.inputFile_tt = jsonInfo[WJetsConfig.name]['file_tt']
WJetsConfig.inputFile_et = jsonInfo[WJetsConfig.name]['file_et']
WJetsConfig.inputFile_mt = jsonInfo[WJetsConfig.name]['file_mt']



crossSectionWeight.XS = jsonInfo[WJetsConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WJetsConfig.name]['forcedGenWeight']
except ValueError:
    crossSectionWeight.forcedGenWeight = None
 
WJetsConfig.listOfWeights = list
