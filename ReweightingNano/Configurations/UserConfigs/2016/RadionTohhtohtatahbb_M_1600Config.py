
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


RadionTohhtohtatahbb_M_1600Config = ReweightConfiguration()
RadionTohhtohtatahbb_M_1600Config.name = 'RadionTohhtohtatahbb_M-1600'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
RadionTohhtohtatahbb_M_1600Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(RadionTohhtohtatahbb_M_1600Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

RadionTohhtohtatahbb_M_1600Config.inputFile = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['file']
RadionTohhtohtatahbb_M_1600Config.inputFile_tt = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['file_tt']
RadionTohhtohtatahbb_M_1600Config.inputFile_et = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['file_et']
RadionTohhtohtatahbb_M_1600Config.inputFile_mt = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[RadionTohhtohtatahbb_M_1600Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


RadionTohhtohtatahbb_M_1600Config.listOfWeights = list
