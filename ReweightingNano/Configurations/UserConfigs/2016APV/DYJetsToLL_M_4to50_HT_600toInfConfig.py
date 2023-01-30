
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


DYJetsToLL_M_4to50_HT_600toInfConfig = ReweightConfiguration()
DYJetsToLL_M_4to50_HT_600toInfConfig.name = 'DYJetsToLL_M-4to50_HT-600toInf'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
DYJetsToLL_M_4to50_HT_600toInfConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(DYJetsToLL_M_4to50_HT_600toInfConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DYJetsToLL_M_4to50_HT_600toInfConfig.inputFile = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['file']
#DYJetsToLL_M_4to50_HT_600toInfConfig.inputFile_tt = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['file_tt']
#DYJetsToLL_M_4to50_HT_600toInfConfig.inputFile_et = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['file_et']
#DYJetsToLL_M_4to50_HT_600toInfConfig.inputFile_mt = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYJetsToLL_M_4to50_HT_600toInfConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYJetsToLL_M_4to50_HT_600toInfConfig.listOfWeights = list
