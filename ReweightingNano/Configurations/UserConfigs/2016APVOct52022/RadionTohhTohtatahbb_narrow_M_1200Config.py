
import ROOT
import os
import json
from .weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016APV


RadionTohhTohtatahbb_narrow_M_1200Config = ReweightConfiguration()
RadionTohhTohtatahbb_narrow_M_1200Config.name = 'RadionTohhTohtatahbb_narrow_M-1200'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016APV_Samples.json'
RadionTohhTohtatahbb_narrow_M_1200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/2016APV_Samples.json'

with open(RadionTohhTohtatahbb_narrow_M_1200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

RadionTohhTohtatahbb_narrow_M_1200Config.inputFile = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['file']
#RadionTohhTohtatahbb_narrow_M_1200Config.inputFile_tt = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['file_tt']
#RadionTohhTohtatahbb_narrow_M_1200Config.inputFile_et = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['file_et']
#RadionTohhTohtatahbb_narrow_M_1200Config.inputFile_mt = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016APV'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[RadionTohhTohtatahbb_narrow_M_1200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


RadionTohhTohtatahbb_narrow_M_1200Config.listOfWeights = list
