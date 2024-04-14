import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

muonPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'

def calculateMuonIDWeight(self, theTree):
    muonIDWeight = 1.0
    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        self.pt = theTree.Muon_pt[theTree.index_gMuons[0]]
        self.eta = theTree.Muon_eta[theTree.index_gMuons[0]]
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIDWeight = muonIDWeight*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"sf")
    self.value[0] = muonIDWeight

def calculateMuonIDWeight_Up(self, theTree, uncert):
    muonIDWeight_Up = 1.0
    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        #muonIDWeight_Up = muonIDWeight_Up*self.evaluator["NUM_LooseID_DEN_genTracks"].evaluate(self.year,abs(theTree.Muon_eta[theTree.index_gMuons[i]]),theTree.Muon_pt[theTree.index_gMuons[i]],"systup")
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIDWeight_Up = muonIDWeight_Up*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"systup")

    self.uncertaintyVariationArrays[uncert][0] = muonIDWeight_Up

def calculateMuonIDWeight_Down(self, theTree, uncert):
    muonIDWeight_Down = 1.0


    #for i in range (theTree.ngood_Muons):
    if (theTree.channel==2):
        #muonIDWeight_Down = muonIDWeight_Down*self.evaluator["NUM_LooseID_DEN_genTracks"].evaluate(self.year,abs(theTree.Muon_eta[theTree.index_gMuons[i]]),theTree.Muon_pt[theTree.index_gMuons[i]],"systdown")
        if (self.pt>=15 and abs(self.eta)<2.4):
            muonIDWeight_Down = muonIDWeight_Down*self.evaluator.evaluate(self.year,abs(self.eta),self.pt,"systdown")
    self.uncertaintyVariationArrays[uncert][0] = muonIDWeight_Down



muonIDWeight_2016 = Weight()
muonIDWeight_2016.name = 'muonIDWeight'
muonIDWeight_2016.year = "2016postVFP_UL"
muonIDWeight_2016.jsonFile = muonPath+'2016postVFP_UL/muon_Z.json.gz'
muonIDWeight_2016.evaluator = _core.CorrectionSet.from_file(muonIDWeight_2016.jsonFile)["NUM_LooseID_DEN_genTracks"]
muonIDWeight_2016.CalculateWeight = calculateMuonIDWeight
muonIDWeight_2016.hasUpDownUncertainties = True
muonIDWeight_2016.uncertaintyVariationList = [
    "muonIDWeight_UP",
    "muonIDWeight_DOWN"
    ]
muonIDWeight_2016.InitUncertaintyVariations()
muonIDWeight_2016.uncertaintyVariationFunctions = {
    "muonIDWeight_UP":calculateMuonIDWeight_Up,
    "muonIDWeight_DOWN":calculateMuonIDWeight_Down
}

muonIDWeight_2016APV = Weight()
muonIDWeight_2016APV.name = 'muonIDWeight'
muonIDWeight_2016APV.year = "2016preVFP_UL"
muonIDWeight_2016APV.jsonFile = muonPath+'2016preVFP_UL/muon_Z.json.gz'
muonIDWeight_2016APV.evaluator = _core.CorrectionSet.from_file(muonIDWeight_2016APV.jsonFile)["NUM_LooseID_DEN_genTracks"]
muonIDWeight_2016APV.CalculateWeight = calculateMuonIDWeight
muonIDWeight_2016APV.hasUpDownUncertainties = True
muonIDWeight_2016APV.uncertaintyVariationList = [
    "muonIDWeight_UP",
    "muonIDWeight_DOWN"
    ]
muonIDWeight_2016APV.InitUncertaintyVariations()
muonIDWeight_2016APV.uncertaintyVariationFunctions = {
    "muonIDWeight_UP":calculateMuonIDWeight_Up,
    "muonIDWeight_DOWN":calculateMuonIDWeight_Down
}


muonIDWeight_2017 = Weight()
muonIDWeight_2017.name = 'muonIDWeight'
muonIDWeight_2017.year = "2017_UL"
muonIDWeight_2017.jsonFile = muonPath+'2017_UL/muon_Z.json.gz'
muonIDWeight_2017.evaluator = _core.CorrectionSet.from_file(muonIDWeight_2017.jsonFile)["NUM_LooseID_DEN_genTracks"]
muonIDWeight_2017.CalculateWeight = calculateMuonIDWeight
muonIDWeight_2017.hasUpDownUncertainties = True
muonIDWeight_2017.uncertaintyVariationList = [
    "muonIDWeight_UP",
    "muonIDWeight_DOWN"
    ]
muonIDWeight_2017.InitUncertaintyVariations()
muonIDWeight_2017.uncertaintyVariationFunctions = {
    "muonIDWeight_UP":calculateMuonIDWeight_Up,
    "muonIDWeight_DOWN":calculateMuonIDWeight_Down
}

muonIDWeight_2018 = Weight()
muonIDWeight_2018.name = 'muonIDWeight'
muonIDWeight_2018.year = "2018_UL"
#muonIDWeight_2018.WP = "Loose"
muonIDWeight_2018.jsonFile = muonPath+'2018_UL/muon_Z.json.gz'
muonIDWeight_2018.evaluator = _core.CorrectionSet.from_file(muonIDWeight_2018.jsonFile)["NUM_LooseID_DEN_genTracks"]
muonIDWeight_2018.CalculateWeight = calculateMuonIDWeight
muonIDWeight_2018.hasUpDownUncertainties = True
muonIDWeight_2018.uncertaintyVariationList = [
    "muonIDWeight_UP",
    "muonIDWeight_DOWN"
    ]
muonIDWeight_2018.InitUncertaintyVariations()
muonIDWeight_2018.uncertaintyVariationFunctions = {
    "muonIDWeight_UP":calculateMuonIDWeight_Up,
    "muonIDWeight_DOWN":calculateMuonIDWeight_Down
}