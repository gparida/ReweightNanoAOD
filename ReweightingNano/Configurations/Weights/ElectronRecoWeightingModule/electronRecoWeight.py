import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 

electronPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'

def calculateElectronRecoWeight(self, theTree):
    electronRecoWeight = 1.0

    #for i in range (theTree.ngood_Electrons):
    if (theTree.channel==1):
        self.pt = theTree.Electron_pt[theTree.index_gElectrons[0]]
        self.eta = theTree.Electron_eta[theTree.index_gElectrons[0]]
        if (theTree.Electron_pt[theTree.index_gElectrons[0]]>20):
            electronRecoWeight = electronRecoWeight*self.evaluator.evaluate(self.year,"sf","RecoAbove20",self.eta,self.pt)
        else:
            electronRecoWeight = electronRecoWeight*self.evaluator.evaluate(self.year,"sf","RecoBelow20",self.eta,self.pt)

    self.value[0] = electronRecoWeight

def calculateElectronRecoWeight_Up(self, theTree, uncert):
    electronRecoWeight_Up = 1.0
    if (theTree.channel==1):
        #print (">>channel = ",theTree.channel," >>Pt for the event = ",self.pt," Eta for the event = ",self.eta)
        if (theTree.Electron_pt[theTree.index_gElectrons[0]]>20):
            electronRecoWeight_Up = electronRecoWeight_Up*self.evaluator.evaluate(self.year,"sfup","RecoAbove20",self.eta,self.pt)
        else:
            electronRecoWeight_Up = electronRecoWeight_Up*self.evaluator.evaluate(self.year,"sfup","RecoBelow20",self.eta,self.pt)

    self.uncertaintyVariationArrays[uncert][0] = electronRecoWeight_Up

def calculateElectronRecoWeight_Down(self, theTree, uncert):
    electronRecoWeight_Down = 1.0
    #evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    #for i in range (theTree.ngood_Electrons):
    if (theTree.channel==1):
        if (theTree.Electron_pt[theTree.index_gElectrons[0]]>20):
            electronRecoWeight_Down = electronRecoWeight_Down*self.evaluator.evaluate(self.year,"sfdown","RecoAbove20",self.eta,self.pt)
        else:
            electronRecoWeight_Down = electronRecoWeight_Down*self.evaluator.evaluate(self.year,"sfdown","RecoBelow20",self.eta,self.pt)

    self.uncertaintyVariationArrays[uncert][0] = electronRecoWeight_Down


electronRecoWeight_2016 = Weight()
electronRecoWeight_2016.name = 'electronRecoWeight'
electronRecoWeight_2016.year = "2016postVFP"
electronRecoWeight_2016.jsonFile = electronPath+'2016postVFP_UL/electron.json.gz'
electronRecoWeight_2016.evaluator = _core.CorrectionSet.from_file(electronRecoWeight_2016.jsonFile)["UL-Electron-ID-SF"]
electronRecoWeight_2016.CalculateWeight = calculateElectronRecoWeight
electronRecoWeight_2016.hasUpDownUncertainties = True
electronRecoWeight_2016.uncertaintyVariationList = [
    "electronRecoWeight_UP",
    "electronRecoWeight_DOWN"
    ]
electronRecoWeight_2016.InitUncertaintyVariations()
electronRecoWeight_2016.uncertaintyVariationFunctions = {
    "electronRecoWeight_UP":calculateElectronRecoWeight_Up,
    "electronRecoWeight_DOWN":calculateElectronRecoWeight_Down
}


electronRecoWeight_2016APV = Weight()
electronRecoWeight_2016APV.name = 'electronRecoWeight'
electronRecoWeight_2016APV.year = "2016preVFP"
electronRecoWeight_2016APV.jsonFile = electronPath+'2016preVFP_UL/electron.json.gz'
electronRecoWeight_2016APV.evaluator = _core.CorrectionSet.from_file(electronRecoWeight_2016APV.jsonFile)["UL-Electron-ID-SF"]
electronRecoWeight_2016APV.CalculateWeight = calculateElectronRecoWeight
electronRecoWeight_2016APV.hasUpDownUncertainties = True
electronRecoWeight_2016APV.uncertaintyVariationList = [
    "electronRecoWeight_UP",
    "electronRecoWeight_DOWN"
    ]
electronRecoWeight_2016APV.InitUncertaintyVariations()
electronRecoWeight_2016APV.uncertaintyVariationFunctions = {
    "electronRecoWeight_UP":calculateElectronRecoWeight_Up,
    "electronRecoWeight_DOWN":calculateElectronRecoWeight_Down
}


electronRecoWeight_2017 = Weight()
electronRecoWeight_2017.name = 'electronRecoWeight'
electronRecoWeight_2017.year = "2017"
electronRecoWeight_2017.jsonFile = electronPath+'2017_UL/electron.json.gz'
electronRecoWeight_2017.evaluator = _core.CorrectionSet.from_file(electronRecoWeight_2017.jsonFile)["UL-Electron-ID-SF"]
electronRecoWeight_2017.CalculateWeight = calculateElectronRecoWeight
electronRecoWeight_2017.hasUpDownUncertainties = True
electronRecoWeight_2017.uncertaintyVariationList = [
    "electronRecoWeight_UP",
    "electronRecoWeight_DOWN"
    ]
electronRecoWeight_2017.InitUncertaintyVariations()
electronRecoWeight_2017.uncertaintyVariationFunctions = {
    "electronRecoWeight_UP":calculateElectronRecoWeight_Up,
    "electronRecoWeight_DOWN":calculateElectronRecoWeight_Down
}


electronRecoWeight_2018 = Weight()
electronRecoWeight_2018.name = 'electronRecoWeight'
electronRecoWeight_2018.year = "2018"
electronRecoWeight_2018.jsonFile = electronPath+'2018_UL/electron.json.gz'
electronRecoWeight_2018.evaluator = _core.CorrectionSet.from_file(electronRecoWeight_2018.jsonFile)["UL-Electron-ID-SF"]
electronRecoWeight_2018.CalculateWeight = calculateElectronRecoWeight
electronRecoWeight_2018.hasUpDownUncertainties = True
electronRecoWeight_2018.uncertaintyVariationList = [
    "electronRecoWeight_UP",
    "electronRecoWeight_DOWN"
    ]
electronRecoWeight_2018.InitUncertaintyVariations()
electronRecoWeight_2018.uncertaintyVariationFunctions = {
    "electronRecoWeight_UP":calculateElectronRecoWeight_Up,
    "electronRecoWeight_DOWN":calculateElectronRecoWeight_Down
}