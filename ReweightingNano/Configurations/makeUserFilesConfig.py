import json
import os


string_out = """
import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
#from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016


{refinedName}Config = ReweightConfiguration()
{refinedName}Config.name = '{Name}'
#QCD_Pt_15to30Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
{refinedName}Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/MetaData/2016_Samples_25Jan.json'

with open({refinedName}Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[{refinedName}Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

{refinedName}Config.inputFile = jsonInfo[{refinedName}Config.name]['file']
{refinedName}Config.inputFile_tt = jsonInfo[{refinedName}Config.name]['file_tt']
{refinedName}Config.inputFile_et = jsonInfo[{refinedName}Config.name]['file_et']
{refinedName}Config.inputFile_mt = jsonInfo[{refinedName}Config.name]['file_mt']


crossSectionWeight.XS = jsonInfo[{refinedName}Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[{refinedName}Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


{refinedName}Config.listOfWeights = list
"""

with open(os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples_25Jan.json') as jsonFile:
    data = json.load(jsonFile)

keys = data.keys()
#save_path = '/UserConfigs/2016'

for name in keys:
    with open('UserConfigs/2016/'+name.replace("-","_")+'Config.py','w+') as file_out:
        file_out.write(string_out.format(refinedName=name.replace("-","_"),Name=name))


