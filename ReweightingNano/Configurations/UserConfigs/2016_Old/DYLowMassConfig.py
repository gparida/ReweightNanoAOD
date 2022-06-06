import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

DYLowMassConfig = ReweightConfiguration()
DYLowMassConfig.name = 'DYLowMass'
#DYLowMassConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYLowMassConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(DYLowMassConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYLowMassConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DYLowMassConfig.inputFile = jsonInfo[DYLowMassConfig.name]['file']
DYLowMassConfig.inputFile_tt = jsonInfo[DYLowMassConfig.name]['file_tt']
DYLowMassConfig.inputFile_et = jsonInfo[DYLowMassConfig.name]['file_et']
DYLowMassConfig.inputFile_mt = jsonInfo[DYLowMassConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYLowMassConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYLowMassConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYLowMassConfig.listOfWeights = list
