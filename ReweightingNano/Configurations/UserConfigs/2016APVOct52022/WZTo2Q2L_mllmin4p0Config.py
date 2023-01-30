
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


WZTo2Q2L_mllmin4p0Config = ReweightConfiguration()
WZTo2Q2L_mllmin4p0Config.name = 'WZTo2Q2L_mllmin4p0'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
WZTo2Q2L_mllmin4p0Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(WZTo2Q2L_mllmin4p0Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

WZTo2Q2L_mllmin4p0Config.inputFile = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['file']
#WZTo2Q2L_mllmin4p0Config.inputFile_tt = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['file_tt']
#WZTo2Q2L_mllmin4p0Config.inputFile_et = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['file_et']
#WZTo2Q2L_mllmin4p0Config.inputFile_mt = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[WZTo2Q2L_mllmin4p0Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


WZTo2Q2L_mllmin4p0Config.listOfWeights = list
