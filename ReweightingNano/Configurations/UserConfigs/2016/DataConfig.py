
import ROOT
import os
import json
from weightList import *

#from Configurations.ConfigDefinition import ReweightConfiguration
#from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


DataConfig = ReweightConfiguration()
DataConfig.name = 'Data'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
DataConfig.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json'

with open(DataConfig.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[DataConfig.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

DataConfig.inputFile = jsonInfo[DataConfig.name]['file']
DataConfig.inputFile_tt = jsonInfo[DataConfig.name]['file_tt']
DataConfig.inputFile_et = jsonInfo[DataConfig.name]['file_et']
DataConfig.inputFile_mt = jsonInfo[DataConfig.name]['file_mt']


#crossSectionWeight.XS = jsonInfo[DataConfig.name]['XS'] * 1e-12 #XS in pb
#crossSectionWeight.timePeriod = '2016'
#crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
#try:
#    crossSectionWeight.forcedGenWeight = jsonInfo[DataConfig.name]['forcedGenWeight']
#except KeyError:
#    crossSectionWeight.forcedGenWeight = None


DataConfig.listOfWeights = []
