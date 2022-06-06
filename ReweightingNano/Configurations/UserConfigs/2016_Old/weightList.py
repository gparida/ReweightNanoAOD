from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016
from Configurations.Weights.TauIDModule.TauIDWeight import tauIDWeight_2016 as tauIDWeight

list=[crossSectionWeight,
    pileupWeight_2016,
    tauIDWeight]