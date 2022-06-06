import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

QCD_Pt_1800to2400Config = ReweightConfiguration()
QCD_Pt_1800to2400Config.name = 'QCD_Pt_1800to2400'
#QCD_Pt_1800to2400Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
QCD_Pt_1800to2400Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'
with open(QCD_Pt_1800to2400Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_Pt_1800to2400Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

QCD_Pt_1800to2400Config.inputFile = jsonInfo[QCD_Pt_1800to2400Config.name]['file']
QCD_Pt_1800to2400Config.inputFile_tt = jsonInfo[QCD_Pt_1800to2400Config.name]['file_tt']
QCD_Pt_1800to2400Config.inputFile_et = jsonInfo[QCD_Pt_1800to2400Config.name]['file_et']
QCD_Pt_1800to2400Config.inputFile_mt = jsonInfo[QCD_Pt_1800to2400Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[QCD_Pt_1800to2400Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_Pt_1800to2400Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_Pt_1800to2400Config.listOfWeights = list
