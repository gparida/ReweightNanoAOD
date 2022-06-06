
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


DYJetsToLL_M_10to50Config = ReweightConfiguration()
DYJetsToLL_M_10to50Config.name = 'DYJetsToLL_M-10to50'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYJetsToLL_M_10to50Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(DYJetsToLL_M_10to50Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYJetsToLL_M_10to50Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DYJetsToLL_M_10to50Config.inputFile = jsonInfo[DYJetsToLL_M_10to50Config.name]['file']
DYJetsToLL_M_10to50Config.inputFile_tt = jsonInfo[DYJetsToLL_M_10to50Config.name]['file_tt']
DYJetsToLL_M_10to50Config.inputFile_et = jsonInfo[DYJetsToLL_M_10to50Config.name]['file_et']
DYJetsToLL_M_10to50Config.inputFile_mt = jsonInfo[DYJetsToLL_M_10to50Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[DYJetsToLL_M_10to50Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYJetsToLL_M_10to50Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


DYJetsToLL_M_10to50Config.listOfWeights = list
