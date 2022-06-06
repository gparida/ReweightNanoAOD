import ROOT
import json
from Configurations.Weights.WeightDefinition import Weight as Weight



#def CalculateCrossSectionWeight(self,theTree):
#    crossSectionWeight = 1.0
#    if self.year == "2016":
#        #LHCLumi = 36.33e15
#        LHCLumi = 16.8e15
#    elif self.year == "2016APV":
#        LHCLumi = 19.5e15
#    elif self.year == "2017":
#        LHCLumi = 41.8e15
#    elif self.year == "2018":
#    	LHCLumi = 59.83e15
#
#
#    if self.year == '2016':
#        crossSections = {
#           "DYlow":15890e-12,
#		   "DY":5398e-12,
#		   "QCD_Pt_1000to1400":7.465e-12,
#		   "QCD_Pt_120to170":407700e-12,
#		   "QCD_Pt_1400to1800":0.6487e-12,
#		   "QCD_Pt_15to30.root":1244000000e-12,
#		   "QCD_Pt_170to300":103700e-12,
#		   "QCD_Pt_1800to2400":0.08734e-12,
#		   "QCD_Pt_2400to3200":0.005237e-12,
#		   "QCD_Pt_300to470":6826e-12,
#		   "QCD_Pt_30to50":106500000e-12,
#		   "QCD_Pt_3200toInf":0.0001352e-12,
#		   "QCD_Pt_470to600":551.2e-12,
#		   "QCD_Pt_50to80":15700000e-12,
#		   "QCD_Pt_600to800":156.7e-12,
#		   "QCD_Pt_800to1000":26.25e-12,
#		   "QCD_Pt_80to120":2346000e-12,
#		   "ST_s-channel_4f":3.549e-12,
#		   "TTTo2L2Nu":687.1e-12,
#		   "TTToHadronic":687.1e-12,
#		   "TTToSemiLeptonic":687.1e-12,
#		   "W":53870e-12,
#		   "WW":75.95e-12,
#		   "WZ":27.6e-12,
#		   "ZZ":12.17e-12,
#        }
#    crossSectionWeighting = (crossSections[self.sample] * LHCLumi)/self.totalEvents
#    crossSectionWeighting = crossSectionWeighting * theTree.genWeight
#    self.value[0] = crossSectionWeighting
#
#crossSectionWeight = Weight()
#crossSectionWeight.name = 'CrossSectionWeighting'
#crossSectionWeight.CalculateWeight = CalculateCrossSectionWeight
 

def calculateCrossSectionWeight(self, theTree):
    crossSectionWeighting = 1.0
    if self.timePeriod == '2016': #not fond of having the configuration spread out like this
        LHCLumi =  16.81e15
    elif self.timePeriod == '2016APV':
        LHCLumi = 19.52e15
    elif self.timePeriod == '2017':
        LHCLumi = 41.48e15
    elif self.timePeriod == '2018':
        LHCLumi = 59.83e15
    else:
        raise RuntimeError('Found unknown or absent time period for XS weights')
        
    crossSectionWeighting = (self.XS * LHCLumi) / self.totalNumberOfEvents

    genWeighting = 1.0
#    if not self.forcedGenWeight == None:
#        genWeighting = self.forcedGenWeight
#    else:
#        genWeighting = theTree.genWeight
#    self.value[0] = crossSectionWeighting * genWeighting
    if theTree.genWeight > 0:
        genWeighting = 1.0
    elif theTree.genWeight < 0:
        genWeighting = -1.0
    
    self.value[0] = crossSectionWeighting * genWeighting
    
    

crossSectionWeight = Weight() # creating an instance of the weight class
crossSectionWeight.name = 'crossSectionWeighting' #filling up the different attributes of the weight class which were previously empyty
crossSectionWeight.CalculateWeight = calculateCrossSectionWeight #This calculate weight function - the way to calculate xs weight
crossSectionWeight.forcedGenWeight = None