
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


QCD_HT700to1000Config = ReweightConfiguration()
QCD_HT700to1000Config.name = 'QCD_HT700to1000'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
QCD_HT700to1000Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(QCD_HT700to1000Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[QCD_HT700to1000Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

QCD_HT700to1000Config.inputFile = jsonInfo[QCD_HT700to1000Config.name]['file']
#QCD_HT700to1000Config.inputFile_tt = jsonInfo[QCD_HT700to1000Config.name]['file_tt']
#QCD_HT700to1000Config.inputFile_et = jsonInfo[QCD_HT700to1000Config.name]['file_et']
#QCD_HT700to1000Config.inputFile_mt = jsonInfo[QCD_HT700to1000Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[QCD_HT700to1000Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[QCD_HT700to1000Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


QCD_HT700to1000Config.listOfWeights = list
