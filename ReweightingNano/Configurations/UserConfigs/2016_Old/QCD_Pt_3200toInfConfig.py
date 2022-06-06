import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

QCD_Pt_3200toInfConfig = ReweightConfiguration()
QCD_Pt_3200toInfConfig.name = 'QCD_Pt_3200toInf'
#QCD_Pt_3200toInfConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
QCD_Pt_3200toInfConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'
with open(QCD_Pt_3200toInfConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_Pt_3200toInfConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

QCD_Pt_3200toInfConfig.inputFile = jsonInfo[QCD_Pt_3200toInfConfig.name]['file']
QCD_Pt_3200toInfConfig.inputFile_tt = jsonInfo[QCD_Pt_3200toInfConfig.name]['file_tt']
QCD_Pt_3200toInfConfig.inputFile_et = jsonInfo[QCD_Pt_3200toInfConfig.name]['file_et']
QCD_Pt_3200toInfConfig.inputFile_mt = jsonInfo[QCD_Pt_3200toInfConfig.name]['file_mt']




crossSectionWeight.XS = jsonInfo[QCD_Pt_3200toInfConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_Pt_3200toInfConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_Pt_3200toInfConfig.listOfWeights = list
