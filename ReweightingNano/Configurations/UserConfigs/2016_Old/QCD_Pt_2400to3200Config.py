import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

QCD_Pt_2400to3200Config = ReweightConfiguration()
QCD_Pt_2400to3200Config.name = 'QCD_Pt_2400to3200'
#QCD_Pt_2400to3200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
QCD_Pt_2400to3200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(QCD_Pt_2400to3200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_Pt_2400to3200Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

QCD_Pt_2400to3200Config.inputFile = jsonInfo[QCD_Pt_2400to3200Config.name]['file']
QCD_Pt_2400to3200Config.inputFile_tt = jsonInfo[QCD_Pt_2400to3200Config.name]['file_tt']
QCD_Pt_2400to3200Config.inputFile_et = jsonInfo[QCD_Pt_2400to3200Config.name]['file_et']
QCD_Pt_2400to3200Config.inputFile_mt = jsonInfo[QCD_Pt_2400to3200Config.name]['file_mt']

crossSectionWeight.XS = jsonInfo[QCD_Pt_2400to3200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_Pt_2400to3200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_Pt_2400to3200Config.listOfWeights = list
