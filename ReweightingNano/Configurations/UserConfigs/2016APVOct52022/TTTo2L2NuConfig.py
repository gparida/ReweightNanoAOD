
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


TTTo2L2NuConfig = ReweightConfiguration()
TTTo2L2NuConfig.name = 'TTTo2L2Nu'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
TTTo2L2NuConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(TTTo2L2NuConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[TTTo2L2NuConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

TTTo2L2NuConfig.inputFile = jsonInfo[TTTo2L2NuConfig.name]['file']
#TTTo2L2NuConfig.inputFile_tt = jsonInfo[TTTo2L2NuConfig.name]['file_tt']
#TTTo2L2NuConfig.inputFile_et = jsonInfo[TTTo2L2NuConfig.name]['file_et']
#TTTo2L2NuConfig.inputFile_mt = jsonInfo[TTTo2L2NuConfig.name]['file_mt']


crossSectionWeight.XS = jsonInfo[TTTo2L2NuConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[TTTo2L2NuConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


TTTo2L2NuConfig.listOfWeights = list
