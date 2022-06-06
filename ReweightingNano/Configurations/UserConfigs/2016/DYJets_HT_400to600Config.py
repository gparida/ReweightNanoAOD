
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


DYJets_HT_400to600Config = ReweightConfiguration()
DYJets_HT_400to600Config.name = 'DYJets_HT-400to600'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYJets_HT_400to600Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(DYJets_HT_400to600Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYJets_HT_400to600Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DYJets_HT_400to600Config.inputFile = jsonInfo[DYJets_HT_400to600Config.name]['file']
DYJets_HT_400to600Config.inputFile_tt = jsonInfo[DYJets_HT_400to600Config.name]['file_tt']
DYJets_HT_400to600Config.inputFile_et = jsonInfo[DYJets_HT_400to600Config.name]['file_et']
DYJets_HT_400to600Config.inputFile_mt = jsonInfo[DYJets_HT_400to600Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYJets_HT_400to600Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYJets_HT_400to600Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYJets_HT_400to600Config.listOfWeights = list
