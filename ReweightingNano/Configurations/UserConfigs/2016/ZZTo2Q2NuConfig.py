
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


ZZTo2Q2NuConfig = ReweightConfiguration()
ZZTo2Q2NuConfig.name = 'ZZTo2Q2Nu'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
ZZTo2Q2NuConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(ZZTo2Q2NuConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[ZZTo2Q2NuConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

ZZTo2Q2NuConfig.inputFile = jsonInfo[ZZTo2Q2NuConfig.name]['file']
ZZTo2Q2NuConfig.inputFile_tt = jsonInfo[ZZTo2Q2NuConfig.name]['file_tt']
ZZTo2Q2NuConfig.inputFile_et = jsonInfo[ZZTo2Q2NuConfig.name]['file_et']
ZZTo2Q2NuConfig.inputFile_mt = jsonInfo[ZZTo2Q2NuConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[ZZTo2Q2NuConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[ZZTo2Q2NuConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


ZZTo2Q2NuConfig.listOfWeights = list
