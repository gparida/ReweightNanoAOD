import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight


triggerWeightPath = os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/TriggerSF/' # path where the SF root file is

def calculateTriggerWeight(self, theTree):
    triggerWeighting = 1.0
    #print ("MET in the event",theTree.METcorrected_pt)

    #Context by Ganesh
    #GetNbinsX() - gives the final bin index. GetNbinsX() + 1 gives us the overflow bin

    if (theTree.METcorrected_pt >= 500):
        #print ("The trigger Scale Factor is for MET > 1000 = ", self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)))
        triggerWeighting = self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX())

    else:
        #print ("The trigger Scale Factor is = ", self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)))
        triggerWeighting = self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt))


    self.value[0] = triggerWeighting

def calculateTriggerWeight_Up(self, theTree, uncert):
    triggerWeighting_Up = 1.0

    if (theTree.METcorrected_pt >= 500):
        #triggerWeighting_Up = self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX()) + 0.02*self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX())
        triggerWeighting_Up = self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX()) + 0.50*(self.sfHisto.GetBinError(self.sfHisto.GetNbinsX()))

    else:
        #triggerWeighting_Up = self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)) + 0.02*self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt))
        triggerWeighting_Up = self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)) + 0.50*(self.sfHisto.GetBinError(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)))

    self.uncertaintyVariationArrays[uncert][0] = triggerWeighting_Up



def calculateTriggerWeight_Down(self, theTree, uncert):
    triggerWeighting_Down = 1.0

    #If the MET is above a certain value (here it is 500 GeV)
    if (theTree.METcorrected_pt >= 500):
        #triggerWeighting_Down = self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX()) - 0.02*self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX())
        triggerWeighting_Down = self.sfHisto.GetBinContent(self.sfHisto.GetNbinsX()) - 0.50*(self.sfHisto.GetBinError(self.sfHisto.GetNbinsX()))

    else:
        #triggerWeighting_Down = self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)) - 0.02*self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt))
        triggerWeighting_Down = self.sfHisto.GetBinContent(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)) - 0.50*(self.sfHisto.GetBinError(self.sfHisto.GetXaxis().FindBin(theTree.METcorrected_pt)))

    self.uncertaintyVariationArrays[uncert][0] = triggerWeighting_Down



triggerWeight_2016 = Weight()
triggerWeight_2016.name = 'triggerWeight'
triggerWeight_2016.sfFilePath = triggerWeightPath+'2016_MetTriggerSFs.root'
#triggerWeight_2016.sfFilePath = 'MetTriggerSFs.root'
triggerWeight_2016.sfHistoFile = ROOT.TFile(triggerWeight_2016.sfFilePath)
triggerWeight_2016.sfHistoDir = triggerWeight_2016.sfHistoFile.GetDirectory("SF")
triggerWeight_2016.sfHisto = triggerWeight_2016.sfHistoDir.Get("MET_SF")
triggerWeight_2016.CalculateWeight = calculateTriggerWeight
triggerWeight_2016.hasUpDownUncertainties = True
triggerWeight_2016.uncertaintyVariationList = ["triggerWeight_UP","triggerWeight_DOWN"]
triggerWeight_2016.InitUncertaintyVariations()
triggerWeight_2016.uncertaintyVariationFunctions = {
    "triggerWeight_UP":calculateTriggerWeight_Up,
    "triggerWeight_DOWN":calculateTriggerWeight_Down
}


triggerWeight_2016APV = Weight()
triggerWeight_2016APV.name = 'triggerWeight'
triggerWeight_2016APV.sfFilePath = triggerWeightPath+'2016APV_MetTriggerSFs.root'
#triggerWeight_2016APV.sfFilePath = 'MetTriggerSFs.root'
triggerWeight_2016APV.sfHistoFile = ROOT.TFile(triggerWeight_2016APV.sfFilePath)
triggerWeight_2016APV.sfHistoDir = triggerWeight_2016APV.sfHistoFile.GetDirectory("SF")
triggerWeight_2016APV.sfHisto = triggerWeight_2016APV.sfHistoDir.Get("MET_SF")
triggerWeight_2016APV.CalculateWeight = calculateTriggerWeight
triggerWeight_2016APV.hasUpDownUncertainties = True
triggerWeight_2016APV.uncertaintyVariationList = ["triggerWeight_UP","triggerWeight_DOWN"]
triggerWeight_2016APV.InitUncertaintyVariations()
triggerWeight_2016APV.uncertaintyVariationFunctions = {
    "triggerWeight_UP":calculateTriggerWeight_Up,
    "triggerWeight_DOWN":calculateTriggerWeight_Down
}


triggerWeight_2017 = Weight()
triggerWeight_2017.name = 'triggerWeight'
triggerWeight_2017.sfFilePath = triggerWeightPath+'2017_MetTriggerSFs.root'
#triggerWeight_2017.sfFilePath = 'MetTriggerSFs.root'
triggerWeight_2017.sfHistoFile = ROOT.TFile(triggerWeight_2017.sfFilePath)
triggerWeight_2017.sfHistoDir = triggerWeight_2017.sfHistoFile.GetDirectory("SF")
triggerWeight_2017.sfHisto = triggerWeight_2017.sfHistoDir.Get("MET_SF")
triggerWeight_2017.CalculateWeight = calculateTriggerWeight
triggerWeight_2017.hasUpDownUncertainties = True
triggerWeight_2017.uncertaintyVariationList = ["triggerWeight_UP","triggerWeight_DOWN"]
triggerWeight_2017.InitUncertaintyVariations()
triggerWeight_2017.uncertaintyVariationFunctions = {
    "triggerWeight_UP":calculateTriggerWeight_Up,
    "triggerWeight_DOWN":calculateTriggerWeight_Down
}


triggerWeight_2018 = Weight()
triggerWeight_2018.name = 'triggerWeight'
triggerWeight_2018.sfFilePath = triggerWeightPath+'2018_MetTriggerSFs.root'
#triggerWeight_2018.sfFilePath = 'MetTriggerSFs.root'
triggerWeight_2018.sfHistoFile = ROOT.TFile(triggerWeight_2018.sfFilePath)
triggerWeight_2018.sfHistoDir = triggerWeight_2018.sfHistoFile.GetDirectory("SF")
triggerWeight_2018.sfHisto = triggerWeight_2018.sfHistoDir.Get("MET_SF")
triggerWeight_2018.CalculateWeight = calculateTriggerWeight
triggerWeight_2018.hasUpDownUncertainties = True
triggerWeight_2018.uncertaintyVariationList = ["triggerWeight_UP","triggerWeight_DOWN"]
triggerWeight_2018.InitUncertaintyVariations()
triggerWeight_2018.uncertaintyVariationFunctions = {
    "triggerWeight_UP":calculateTriggerWeight_Up,
    "triggerWeight_DOWN":calculateTriggerWeight_Down
}


