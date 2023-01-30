import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core
#from Configurations.Weights import b2gWeightPath

b2gWeightPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/LUM/'

def calculatePileupWeight(self, theTree):
    pileupWeighting = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)


    pileupWeighting = evaluator["Collisions16_UltraLegacy_goldenJSON"].evaluate(theTree.Pileup_nTrueInt,"nominal")
    self.value[0] = pileupWeighting

def calculatePileupWeight_Up(self, theTree, uncert):
    pileupWeighting_Up = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    pileupWeighting_Up = evaluator["Collisions16_UltraLegacy_goldenJSON"].evaluate(theTree.Pileup_nTrueInt,"up")
    self.uncertaintyVariationArrays[uncert][0] = pileupWeighting_Up

def calculatePileupWeight_Down(self, theTree, uncert):
    pileupWeighting_Down = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)
    
    pileupWeighting_Down = evaluator["Collisions16_UltraLegacy_goldenJSON"].evaluate(theTree.Pileup_nTrueInt,"down")
    self.uncertaintyVariationArrays[uncert][0] = pileupWeighting_Down





pileupWeight_2016 = Weight()
pileupWeight_2016.name = 'pileupWeighting'
pileupWeight_2016.jsonFile = b2gWeightPath+'2016postVFP_UL/puWeights.json.gz'
pileupWeight_2016.CalculateWeight = calculatePileupWeight
pileupWeight_2016.hasUpDownUncertainties = True
pileupWeight_2016.uncertaintyVariationList = [
    "pileupWeight_UP",
    "pileupWeight_DOWN"
    ]
pileupWeight_2016.InitUncertaintyVariations()
pileupWeight_2016.uncertaintyVariationFunctions = {
    "pileupWeight_UP":calculatePileupWeight_Up,
    "pileupWeight_DOWN":calculatePileupWeight_Down
}


pileupWeight_2016APV = Weight()
pileupWeight_2016APV.name = 'pileupWeighting'
pileupWeight_2016APV.jsonFile = b2gWeightPath+'2016preVFP_UL/puWeights.json.gz'
pileupWeight_2016APV.CalculateWeight = calculatePileupWeight
pileupWeight_2016APV.hasUpDownUncertainties = True
pileupWeight_2016APV.uncertaintyVariationList = [
    "pileupWeight_UP",
    "pileupWeight_DOWN"
    ]
pileupWeight_2016APV.InitUncertaintyVariations()
pileupWeight_2016APV.uncertaintyVariationFunctions = {
    "pileupWeight_UP":calculatePileupWeight_Up,
    "pileupWeight_DOWN":calculatePileupWeight_Down
}


