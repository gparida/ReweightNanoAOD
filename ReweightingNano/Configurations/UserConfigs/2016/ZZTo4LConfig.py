
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ZZTo4LConfig = ReweightConfiguration()
ZZTo4LConfig.name = 'ZZTo4L'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ZZTo4LConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016_Samples.json'

with open(ZZTo4LConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ZZTo4LConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ZZTo4LConfig.inputFile = jsonInfo[ZZTo4LConfig.name]['file']
#ZZTo4LConfig.inputFile_tt = jsonInfo[ZZTo4LConfig.name]['file_tt']
#ZZTo4LConfig.inputFile_et = jsonInfo[ZZTo4LConfig.name]['file_et']
#ZZTo4LConfig.inputFile_mt = jsonInfo[ZZTo4LConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ZZTo4LConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ZZTo4LConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ZZTo4LConfig.listOfWeights = list
