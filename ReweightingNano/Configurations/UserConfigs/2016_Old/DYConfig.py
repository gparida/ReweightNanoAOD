import ROOT
import os
import json
from weightList import *


from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016
from Configurations.Weights.TauIDModule.TauIDWeight import tauIDWeight_2016 as tauIDWeight

DYConfig = ReweightConfiguration()
DYConfig.name = 'DY'
#DYConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DYConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(DYConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DYConfig.name]['file_tt'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

#DYConfig.inputFile = jsonInfo[DYConfig.name]['file']
DYConfig.inputFile = jsonInfo[DYConfig.name]['file']
DYConfig.inputFile_tt = jsonInfo[DYConfig.name]['file_tt']
DYConfig.inputFile_et = jsonInfo[DYConfig.name]['file_et']
DYConfig.inputFile_mt = jsonInfo[DYConfig.name]['file_mt']
#DYConfig.inputFile = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/tt_Channel/allTau_VM_DR_1/DY.root"

crossSectionWeight.XS = jsonInfo[DYConfig.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[DYConfig.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


#DYConfig.listOfWeights = [
#    crossSectionWeight,
#    pileupWeight_2016,
#    tauIDWeight
#]

DYConfig.listOfWeights = list