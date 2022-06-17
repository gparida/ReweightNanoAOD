import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

electronPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'

def calculateElectronSF(self, theTree):
    electronWeight = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    for i in range (len(theTree.gElectron_pt)):
        electronWeight = electronWeight*evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sf",self.WP,theTree.gElectron_eta[i],theTree.gElectron_pt[i])
    
    self.value[0] = electronWeight

def calculateElectronSF_Up(self, theTree, uncert):
    electronWeight_Up = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    for i in range (len(theTree.gElectron_pt)):
        electronWeight_Up = electronWeight_Up*evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sfup",self.WP,theTree.gElectron_eta[i],theTree.gElectron_pt[i])
    self.uncertaintyVariationArrays[uncert][0] = electronWeight_Up

def calculateElectronSF_Down(self, theTree, uncert):
    electronWeight_Down = 1.0
    evaluator = _core.CorrectionSet.from_file(self.jsonFile)
    
    for i in range (len(theTree.gElectron_pt)):
        electronWeight_Down = electronWeight_Down*evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sfdown",self.WP,theTree.gElectron_eta[i],theTree.gElectron_pt[i])
    self.uncertaintyVariationArrays[uncert][0] = electronWeight_Down



electronSF_2016 = Weight()
electronSF_2016.name = 'electronSF'
electronSF_2016.year = "2016postVFP"
electronSF_2016.WP = "Loose"
electronSF_2016.jsonFile = electronPath+'2016postVFP_UL/electron.json.gz'
electronSF_2016.CalculateWeight = calculateElectronSF
electronSF_2016.hasUpDownUncertainties = True
electronSF_2016.uncertaintyVariationList = [
    "electronSF_UP",
    "electronSF_DOWN"
    ]
electronSF_2016.InitUncertaintyVariations()
electronSF_2016.uncertaintyVariationFunctions = {
    "electronSF_UP":calculateElectronSF_Up,
    "electronSF_DOWN":calculateElectronSF_Down
}