import ROOT
from Configurations.Weights.WeightDefinition import Weight as Weight
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
import TauIDFunctions


#uncomment this section when we have finalized our weights for deep boosted Tau
#tauIDWeight_2016 = Weight()
#tauIDWeight_2016.name = 'TauIDWeight'
#tauIDWeight_2016.SFTool = TauIDSFTool("2016Legacy","MVAoldDM2017v2","VLoose")
#tauIDWeight_2016.CalculateWeight = TauIDFunctions.CalculateTauIDWeight
#tauIDWeight_2016.hasUpDownUncertainties = True


#Now this section is implemented when we are using DeepTau for standard Taus and MVAold for Standard taus

tauIDWeight_2016 = Weight()
tauIDWeight_2016.name = 'TauIDWeight'
tauIDWeight_2016.SFTool_boosted = TauIDSFTool("2016Legacy","MVAoldDM2017v2","VLoose")
tauIDWeight_2016.SFTool_standard = TauIDSFTool("UL2016_postVFP","DeepTau2017v2p1VSjet","VVVLoose")
tauIDWeight_2016.CalculateWeight = TauIDFunctions.CalculateTauIDWeight

