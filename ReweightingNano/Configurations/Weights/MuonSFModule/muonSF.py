import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

muonPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'

def calculateMuonSF(self, theTree):
    muonWeight = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    for i in range (len(theTree.gMuon_pt)):
        muonWeight = muonWeight*evaluator["NUM_LooseID_DEN_TrackerMuons"].evaluate(self.year,theTree.gMuon_eta[i],theTree.gMuon_pt[i],"sf")
    
    self.value[0] = muonWeight

def calculateMuonSF_Up(self, theTree, uncert):
    muonWeight_Up = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    for i in range (len(theTree.gMuon_pt)):
        muonWeight_Up = muonWeight_Up*evaluator["NUM_LooseID_DEN_TrackerMuon"].evaluate(self.year,theTree.gMuon_eta[i],theTree.gMuon_pt[i],"systup")
    self.uncertaintyVariationArrays[uncert][0] = muonWeight_Up

def calculateMuonSF_Down(self, theTree, uncert):
    muonWeight_Down = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)
    
    for i in range (len(theTree.gMuon_pt)):
        muonWeight_Down = muonWeight_Down*evaluator["NUM_LooseID_DEN_TrackerMuon"].evaluate(self.year,theTree.gMuon_eta[i],theTree.gMuon_pt[i],"systdown")
    self.uncertaintyVariationArrays[uncert][0] = muonWeight_Down



muonSF_2016 = Weight()
muonSF_2016.name = 'muonSF'
muonSF_2016.year = "2016postVFP_UL"
#muonSF_2016.WP = "Loose"
muonSF_2016.jsonFile = muonPath+'2016postVFP_UL/muon_Z.json.gz'
muonSF_2016.CalculateWeight = calculateMuonSF
muonSF_2016.hasUpDownUncertainties = True
muonSF_2016.uncertaintyVariationList = [
    "muonSF_UP",
    "muonSF_DOWN"
    ]
muonSF_2016.InitUncertaintyVariations()
muonSF_2016.uncertaintyVariationFunctions = {
    "muonSF_UP":calculateMuonSF_Up,
    "muonSF_DOWN":calculateMuonSF_Down
}