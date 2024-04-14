import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

muonPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'

def calculateMuonIsoWeight(self, theTree):
    muonIsoWeight = 1.0
    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        self.pt = theTree.Muon_pt[theTree.index_gMuons[0]]
        self.eta = theTree.Muon_eta[theTree.index_gMuons[0]]
        #print("Muon Pt = ",self.pt)
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIsoWeight = muonIsoWeight*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"sf")
    self.value[0] = muonIsoWeight

def calculateMuonIsoWeight_Up(self, theTree, uncert):
    muonIsoWeight_Up = 1.0
    #evaluator = _core.CorrectionSet.from_file(self.jsonFile)
    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIsoWeight_Up = muonIsoWeight_Up*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"systup")

    self.uncertaintyVariationArrays[uncert][0] = muonIsoWeight_Up

def calculateMuonIsoWeight_Down(self, theTree, uncert):
    muonIsoWeight_Down = 1.0
    #evaluator = _core.CorrectionSet.from_file(self.jsonFile)


    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIsoWeight_Down = muonIsoWeight_Down*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"systdown")

    self.uncertaintyVariationArrays[uncert][0] = muonIsoWeight_Down



muonIsoWeight_2016 = Weight()
muonIsoWeight_2016.name = 'muonIsoWeight'
muonIsoWeight_2016.year = "2016postVFP_UL"
muonIsoWeight_2016.jsonFile = muonPath+'2016postVFP_UL/muon_Z.json.gz'
muonIsoWeight_2016.evaluator = _core.CorrectionSet.from_file(muonIsoWeight_2016.jsonFile)["NUM_LooseRelIso_DEN_LooseID"]
muonIsoWeight_2016.CalculateWeight = calculateMuonIsoWeight
muonIsoWeight_2016.hasUpDownUncertainties = True
muonIsoWeight_2016.uncertaintyVariationList = [
    "muonIsoWeight_UP",
    "muonIsoWeight_DOWN"
    ]
muonIsoWeight_2016.InitUncertaintyVariations()
muonIsoWeight_2016.uncertaintyVariationFunctions = {
    "muonIsoWeight_UP":calculateMuonIsoWeight_Up,
    "muonIsoWeight_DOWN":calculateMuonIsoWeight_Down
}

muonIsoWeight_2016APV = Weight()
muonIsoWeight_2016APV.name = 'muonIsoWeight'
muonIsoWeight_2016APV.year = "2016preVFP_UL"
muonIsoWeight_2016APV.jsonFile = muonPath+'2016preVFP_UL/muon_Z.json.gz'
muonIsoWeight_2016APV.evaluator = _core.CorrectionSet.from_file(muonIsoWeight_2016APV.jsonFile)["NUM_LooseRelIso_DEN_LooseID"]
muonIsoWeight_2016APV.CalculateWeight = calculateMuonIsoWeight
muonIsoWeight_2016APV.hasUpDownUncertainties = True
muonIsoWeight_2016APV.uncertaintyVariationList = [
    "muonIsoWeight_UP",
    "muonIsoWeight_DOWN"
    ]
muonIsoWeight_2016APV.InitUncertaintyVariations()
muonIsoWeight_2016APV.uncertaintyVariationFunctions = {
    "muonIsoWeight_UP":calculateMuonIsoWeight_Up,
    "muonIsoWeight_DOWN":calculateMuonIsoWeight_Down
}


muonIsoWeight_2017 = Weight()
muonIsoWeight_2017.name = 'muonIsoWeight'
muonIsoWeight_2017.year = "2017_UL"
muonIsoWeight_2017.jsonFile = muonPath+'2017_UL/muon_Z.json.gz'
muonIsoWeight_2017.evaluator = _core.CorrectionSet.from_file(muonIsoWeight_2017.jsonFile)["NUM_LooseRelIso_DEN_LooseID"]
muonIsoWeight_2017.CalculateWeight = calculateMuonIsoWeight
muonIsoWeight_2017.hasUpDownUncertainties = True
muonIsoWeight_2017.uncertaintyVariationList = [
    "muonIsoWeight_UP",
    "muonIsoWeight_DOWN"
    ]
muonIsoWeight_2017.InitUncertaintyVariations()
muonIsoWeight_2017.uncertaintyVariationFunctions = {
    "muonIsoWeight_UP":calculateMuonIsoWeight_Up,
    "muonIsoWeight_DOWN":calculateMuonIsoWeight_Down
}

muonIsoWeight_2018 = Weight()
muonIsoWeight_2018.name = 'muonIsoWeight'
muonIsoWeight_2018.year = "2018_UL"
#muonIsoWeight_2018.WP = "Loose"
muonIsoWeight_2018.jsonFile = muonPath+'2018_UL/muon_Z.json.gz'
muonIsoWeight_2018.evaluator = _core.CorrectionSet.from_file(muonIsoWeight_2018.jsonFile)["NUM_LooseRelIso_DEN_LooseID"]
muonIsoWeight_2018.CalculateWeight = calculateMuonIsoWeight
muonIsoWeight_2018.hasUpDownUncertainties = True
muonIsoWeight_2018.uncertaintyVariationList = [
    "muonIsoWeight_UP",
    "muonIsoWeight_DOWN"
    ]
muonIsoWeight_2018.InitUncertaintyVariations()
muonIsoWeight_2018.uncertaintyVariationFunctions = {
    "muonIsoWeight_UP":calculateMuonIsoWeight_Up,
    "muonIsoWeight_DOWN":calculateMuonIsoWeight_Down
}