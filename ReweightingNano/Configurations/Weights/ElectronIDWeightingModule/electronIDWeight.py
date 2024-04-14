import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
from correctionlib import _core 
#from cppyy import addressof, bind_object
#from cppyy.gbl import Abstract, Concrete
import ctypes 

electronPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'

def calculateElectronIDWeight(self, theTree):
    electronIDWeight = 1.0
    #for i in range (theTree.ngood_Electrons):
    if (theTree.channel==1):
        self.pt = theTree.Electron_pt[theTree.index_gElectrons[0]]
        self.eta = theTree.Electron_eta[theTree.index_gElectrons[0]]
        #print (i)
        #print("Number of good ele : ",type(theTree.ngood_Electrons)," : Indices : ",theTree.index_gElectrons[0],theTree.Electron_pt[0]," channel ",theTree.channel,theTree.run, theTree.luminosityBlock,theTree.event)
        #electronIDWeight = electronIDWeight*self.evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sf",self.WP,theTree.Electron_eta[theTree.index_gElectrons[0]],theTree.Electron_pt[theTree.index_gElectrons[0]])
        electronIDWeight = electronIDWeight*self.evaluator.evaluate(self.year,"sf",self.WP,self.eta,self.pt)
    self.value[0] = electronIDWeight

def calculateElectronIDWeight_Up(self, theTree, uncert):
    electronIDWeight_Up = 1.0
    #evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    #for i in range (theTree.ngood_Electrons):
    if (theTree.channel==1):
        #electronIDWeight_Up = electronIDWeight_Up*self.evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sfup",self.WP,theTree.Electron_eta[theTree.index_gElectrons[0]],theTree.Electron_pt[theTree.index_gElectrons[0]])
        electronIDWeight_Up = electronIDWeight_Up*self.evaluator.evaluate(self.year,"sfup",self.WP,self.eta,self.pt)

    self.uncertaintyVariationArrays[uncert][0] = electronIDWeight_Up

def calculateElectronIDWeight_Down(self, theTree, uncert):
    electronIDWeight_Down = 1.0
    #evaluator = _core.CorrectionSet.from_file(self.jsonFile)

    #for i in range (theTree.ngood_Electrons):
    if (theTree.channel==1):
        #electronIDWeight_Down = electronIDWeight_Down*self.evaluator["UL-Electron-ID-SF"].evaluate(self.year,"sfdown",self.WP,theTree.Electron_eta[theTree.index_gElectrons[0]],theTree.Electron_pt[theTree.index_gElectrons[0]])
        electronIDWeight_Down = electronIDWeight_Down*self.evaluator.evaluate(self.year,"sfdown",self.WP,self.eta,self.pt)

    self.uncertaintyVariationArrays[uncert][0] = electronIDWeight_Down


electronIDWeight_2016 = Weight()
electronIDWeight_2016.name = 'electronIDWeight'
electronIDWeight_2016.year = "2016postVFP"
electronIDWeight_2016.WP = "Loose"
electronIDWeight_2016.jsonFile = electronPath+'2016postVFP_UL/electron.json.gz'
electronIDWeight_2016.evaluator = _core.CorrectionSet.from_file(electronIDWeight_2016.jsonFile)["UL-Electron-ID-SF"]
electronIDWeight_2016.CalculateWeight = calculateElectronIDWeight
electronIDWeight_2016.hasUpDownUncertainties = True
electronIDWeight_2016.uncertaintyVariationList = [
    "electronIDWeight_UP",
    "electronIDWeight_DOWN"
    ]
electronIDWeight_2016.InitUncertaintyVariations()
electronIDWeight_2016.uncertaintyVariationFunctions = {
    "electronIDWeight_UP":calculateElectronIDWeight_Up,
    "electronIDWeight_DOWN":calculateElectronIDWeight_Down
}


electronIDWeight_2016APV = Weight()
electronIDWeight_2016APV.name = 'electronIDWeight'
electronIDWeight_2016APV.year = "2016preVFP"
electronIDWeight_2016APV.WP = "Loose"
electronIDWeight_2016APV.jsonFile = electronPath+'2016preVFP_UL/electron.json.gz'
electronIDWeight_2016APV.evaluator = _core.CorrectionSet.from_file(electronIDWeight_2016APV.jsonFile)["UL-Electron-ID-SF"]
electronIDWeight_2016APV.CalculateWeight = calculateElectronIDWeight
electronIDWeight_2016APV.hasUpDownUncertainties = True
electronIDWeight_2016APV.uncertaintyVariationList = [
    "electronIDWeight_UP",
    "electronIDWeight_DOWN"
    ]
electronIDWeight_2016APV.InitUncertaintyVariations()
electronIDWeight_2016APV.uncertaintyVariationFunctions = {
    "electronIDWeight_UP":calculateElectronIDWeight_Up,
    "electronIDWeight_DOWN":calculateElectronIDWeight_Down
}


electronIDWeight_2017 = Weight()
electronIDWeight_2017.name = 'electronIDWeight'
electronIDWeight_2017.year = "2017"
electronIDWeight_2017.WP = "Loose"
electronIDWeight_2017.jsonFile = electronPath+'2017_UL/electron.json.gz'
electronIDWeight_2017.evaluator = _core.CorrectionSet.from_file(electronIDWeight_2017.jsonFile)["UL-Electron-ID-SF"]
electronIDWeight_2017.CalculateWeight = calculateElectronIDWeight
electronIDWeight_2017.hasUpDownUncertainties = True
electronIDWeight_2017.uncertaintyVariationList = [
    "electronIDWeight_UP",
    "electronIDWeight_DOWN"
    ]
electronIDWeight_2017.InitUncertaintyVariations()
electronIDWeight_2017.uncertaintyVariationFunctions = {
    "electronIDWeight_UP":calculateElectronIDWeight_Up,
    "electronIDWeight_DOWN":calculateElectronIDWeight_Down
}


electronIDWeight_2018 = Weight()
electronIDWeight_2018.name = 'electronIDWeight'
electronIDWeight_2018.year = "2018"
electronIDWeight_2018.WP = "Loose"
electronIDWeight_2018.jsonFile = electronPath+'2018_UL/electron.json.gz'
electronIDWeight_2018.evaluator = _core.CorrectionSet.from_file(electronIDWeight_2018.jsonFile)["UL-Electron-ID-SF"]
electronIDWeight_2018.CalculateWeight = calculateElectronIDWeight
electronIDWeight_2018.hasUpDownUncertainties = True
electronIDWeight_2018.uncertaintyVariationList = [
    "electronIDWeight_UP",
    "electronIDWeight_DOWN"
    ]
electronIDWeight_2018.InitUncertaintyVariations()
electronIDWeight_2018.uncertaintyVariationFunctions = {
    "electronIDWeight_UP":calculateElectronIDWeight_Up,
    "electronIDWeight_DOWN":calculateElectronIDWeight_Down
}