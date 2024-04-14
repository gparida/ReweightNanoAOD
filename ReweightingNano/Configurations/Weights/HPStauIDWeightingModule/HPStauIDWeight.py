import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

HPStauPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/TAU/'

def calculateHPStauIDWeight(self, theTree):
    HPStauIDWeight = 1.0
    dmlist = [0,1,2,10,11]
    if (theTree.boost==0):
        for i in range(theTree.ngood_Taus):
            if((theTree.Tau_pt[theTree.index_gTaus[i]]<=140) and ((theTree.Tau_decayMode[theTree.index_gTaus[i]] in dmlist))):
                HPStauIDWeight = HPStauIDWeight*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","nom","dm")
            elif((theTree.Tau_pt[theTree.index_gTaus[i]]>140)):
                HPStauIDWeight = HPStauIDWeight*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","nom","pt")           
    self.value[0] = HPStauIDWeight

def calculateHPStauIDWeight_Up(self, theTree, uncert):
    HPStauIDWeight_Up = 1.0
    dmlist = [0,1,2,10,11]
    if (theTree.boost==0):
        for i in range(theTree.ngood_Taus):
            if((theTree.Tau_pt[theTree.index_gTaus[i]]<=140) and ((theTree.Tau_decayMode[theTree.index_gTaus[i]] in dmlist))):
                HPStauIDWeight_Up = HPStauIDWeight_Up*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","syst_alleras_up","dm")
            elif((theTree.Tau_pt[theTree.index_gTaus[i]]>140)):
                HPStauIDWeight_Up = HPStauIDWeight_Up*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","up","pt")
    self.uncertaintyVariationArrays[uncert][0] = HPStauIDWeight_Up

def calculateHPStauIDWeight_Down(self, theTree, uncert):
    HPStauIDWeight_Down = 1.0
    dmlist = [0,1,2,10,11]

    if (theTree.boost==0):
        for i in range(theTree.ngood_Taus):
            if((theTree.Tau_pt[theTree.index_gTaus[i]]<=140) and ((theTree.Tau_decayMode[theTree.index_gTaus[i]] in dmlist))):
                HPStauIDWeight_Down = HPStauIDWeight_Down*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","syst_alleras_down","dm")
            elif((theTree.Tau_pt[theTree.index_gTaus[i]]>140)):
                HPStauIDWeight_Down = HPStauIDWeight_Down*self.evaluator.evaluate(theTree.Tau_pt[theTree.index_gTaus[i]],theTree.Tau_decayMode[theTree.index_gTaus[i]],theTree.Tau_genPartFlav[theTree.index_gTaus[i]],"Loose","VVLoose","down","pt")
    self.uncertaintyVariationArrays[uncert][0] = HPStauIDWeight_Down



HPStauIDWeight_2016 = Weight()
HPStauIDWeight_2016.name = 'HPStauIDWeight'
HPStauIDWeight_2016.year = "2016postVFP_UL"
HPStauIDWeight_2016.jsonFile = HPStauPath+'2016postVFP_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2016_postVFP.json.gz'
HPStauIDWeight_2016.evaluator = _core.CorrectionSet.from_file(HPStauIDWeight_2016.jsonFile)["DeepTau2018v2p5VSjet"]
HPStauIDWeight_2016.CalculateWeight = calculateHPStauIDWeight
HPStauIDWeight_2016.hasUpDownUncertainties = True
HPStauIDWeight_2016.uncertaintyVariationList = [
    "HPStauIDWeight_UP",
    "HPStauIDWeight_DOWN"
    ]
HPStauIDWeight_2016.InitUncertaintyVariations()
HPStauIDWeight_2016.uncertaintyVariationFunctions = {
    "HPStauIDWeight_UP":calculateHPStauIDWeight_Up,
    "HPStauIDWeight_DOWN":calculateHPStauIDWeight_Down
}

HPStauIDWeight_2016APV = Weight()
HPStauIDWeight_2016APV.name = 'HPStauIDWeight'
HPStauIDWeight_2016APV.year = "2016preVFP_UL"
HPStauIDWeight_2016APV.jsonFile = HPStauPath+'2016preVFP_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2016_preVFP.json.gz'
HPStauIDWeight_2016APV.evaluator = _core.CorrectionSet.from_file(HPStauIDWeight_2016APV.jsonFile)["DeepTau2018v2p5VSjet"]
HPStauIDWeight_2016APV.CalculateWeight = calculateHPStauIDWeight
HPStauIDWeight_2016APV.hasUpDownUncertainties = True
HPStauIDWeight_2016APV.uncertaintyVariationList = [
    "HPStauIDWeight_UP",
    "HPStauIDWeight_DOWN"
    ]
HPStauIDWeight_2016APV.InitUncertaintyVariations()
HPStauIDWeight_2016APV.uncertaintyVariationFunctions = {
    "HPStauIDWeight_UP":calculateHPStauIDWeight_Up,
    "HPStauIDWeight_DOWN":calculateHPStauIDWeight_Down
}


HPStauIDWeight_2017 = Weight()
HPStauIDWeight_2017.name = 'HPStauIDWeight'
HPStauIDWeight_2017.year = "2017_UL"
HPStauIDWeight_2017.jsonFile = HPStauPath+'2017_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2017.json.gz'
HPStauIDWeight_2017.evaluator = _core.CorrectionSet.from_file(HPStauIDWeight_2017.jsonFile)["DeepTau2018v2p5VSjet"]
HPStauIDWeight_2017.CalculateWeight = calculateHPStauIDWeight
HPStauIDWeight_2017.hasUpDownUncertainties = True
HPStauIDWeight_2017.uncertaintyVariationList = [
    "HPStauIDWeight_UP",
    "HPStauIDWeight_DOWN"
    ]
HPStauIDWeight_2017.InitUncertaintyVariations()
HPStauIDWeight_2017.uncertaintyVariationFunctions = {
    "HPStauIDWeight_UP":calculateHPStauIDWeight_Up,
    "HPStauIDWeight_DOWN":calculateHPStauIDWeight_Down
}

HPStauIDWeight_2018 = Weight()
HPStauIDWeight_2018.name = 'HPStauIDWeight'
HPStauIDWeight_2018.year = "2018_UL"
#HPStauIDWeight_2018.WP = "Loose"
HPStauIDWeight_2018.jsonFile = HPStauPath+'2018_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2018.json.gz'
HPStauIDWeight_2018.evaluator = _core.CorrectionSet.from_file(HPStauIDWeight_2018.jsonFile)["DeepTau2018v2p5VSjet"]
HPStauIDWeight_2018.CalculateWeight = calculateHPStauIDWeight
HPStauIDWeight_2018.hasUpDownUncertainties = True
HPStauIDWeight_2018.uncertaintyVariationList = [
    "HPStauIDWeight_UP",
    "HPStauIDWeight_DOWN"
    ]
HPStauIDWeight_2018.InitUncertaintyVariations()
HPStauIDWeight_2018.uncertaintyVariationFunctions = {
    "HPStauIDWeight_UP":calculateHPStauIDWeight_Up,
    "HPStauIDWeight_DOWN":calculateHPStauIDWeight_Down
}