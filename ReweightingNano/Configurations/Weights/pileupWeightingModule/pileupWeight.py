import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
#from Configurations.Weights import b2gWeightPath

b2gWeightPath = os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/PileupReweighting/'

def calculatePileupWeight(self, theTree):
    pileupWeighting = 1.0

    try:

        pileupWeighting = self.dataHisto.GetBinContent(self.dataHisto.GetXaxis().FindBin(theTree.Pileup_nPU)) / self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU))

    except ZeroDivisionError:
        print ("Zero Division Error has occured in NOMINAL ","Numerator = ",self.dataHisto.GetBinContent(self.dataHisto.GetXaxis().FindBin(theTree.Pileup_nPU)),"Denominator = ", self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU)))
        pileupWeighting = 1.0

    self.value[0] = pileupWeighting

def calculatePileupWeight_Up(self, theTree, uncert):
    pileupWeighting_Up = 1.0

    try:

        pileupWeighting_Up = self.dataHistoUp.GetBinContent(self.dataHistoUp.GetXaxis().FindBin(theTree.Pileup_nPU)) / self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU))
    
    except ZeroDivisionError:
        print ("Zero Error has occured in UP ","Numerator = ", self.dataHistoUp.GetXaxis().FindBin(theTree.Pileup_nPU), "Denominator = ",self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU)))
    
    self.uncertaintyVariationArrays[uncert][0] = pileupWeighting_Up

def calculatePileupWeight_Down(self, theTree, uncert):
    pileupWeighting_Down = 1.0

    try:
        pileupWeighting_Down = self.dataHistoDown.GetBinContent(self.dataHistoDown.GetXaxis().FindBin(theTree.Pileup_nPU)) / self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU))
    
    except:
        print ("Zero Error has occured in DOWN","Numerator = ",self.dataHistoDown.GetXaxis().FindBin(theTree.Pileup_nPU),"Denominator = ",self.mcHisto.GetBinContent(self.mcHisto.GetXaxis().FindBin(theTree.Pileup_nPU)))

    self.uncertaintyVariationArrays[uncert][0] = pileupWeighting_Down





pileupWeight_2016 = Weight()
pileupWeight_2016.name = 'pileupWeighting'
pileupWeight_2016.mcHistoFilePath = b2gWeightPath+'mcPileupUL2016.root'
pileupWeight_2016.mcHistoFile = ROOT.TFile(pileupWeight_2016.mcHistoFilePath)
pileupWeight_2016.mcHisto = pileupWeight_2016.mcHistoFile.Get('pu_mc')
pileupWeight_2016.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2016-100bins_withVar.root'
pileupWeight_2016.dataHistoFile = ROOT.TFile(pileupWeight_2016.dataHistoFilePath)
pileupWeight_2016.dataHisto = pileupWeight_2016.dataHistoFile.Get('pileup')
pileupWeight_2016.dataHistoUp = pileupWeight_2016.dataHistoFile.Get('pileup_plus')
pileupWeight_2016.dataHistoDown = pileupWeight_2016.dataHistoFile.Get('pileup_minus')
pileupWeight_2016.mcHisto.Scale(1.0/pileupWeight_2016.mcHisto.Integral())
pileupWeight_2016.dataHisto.Scale(1.0/pileupWeight_2016.dataHisto.Integral())
pileupWeight_2016.dataHistoUp.Scale(1.0/pileupWeight_2016.dataHistoUp.Integral())
pileupWeight_2016.dataHistoDown.Scale(1.0/pileupWeight_2016.dataHistoDown.Integral())
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




pileupWeight_2017 = Weight()
pileupWeight_2017.name = 'pileupWeighting'
pileupWeight_2017.mcHistoFilePath = b2gWeightPath+'mcPileupUL2017.root'
pileupWeight_2017.mcHistoFile = ROOT.TFile(pileupWeight_2017.mcHistoFilePath)
pileupWeight_2017.mcHisto = pileupWeight_2017.mcHistoFile.Get('pu_mc')
pileupWeight_2017.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2017-100bins_withVar.root'
pileupWeight_2017.dataHistoFile = ROOT.TFile(pileupWeight_2017.dataHistoFilePath)
pileupWeight_2017.dataHisto = pileupWeight_2017.dataHistoFile.Get('pileup')
pileupWeight_2017.dataHistoUp = pileupWeight_2017.dataHistoFile.Get('pileup_plus')
pileupWeight_2017.dataHistoDown = pileupWeight_2017.dataHistoFile.Get('pileup_minus')
pileupWeight_2017.mcHisto.Scale(1.0/pileupWeight_2017.mcHisto.Integral())
pileupWeight_2017.dataHisto.Scale(1.0/pileupWeight_2017.dataHisto.Integral())
pileupWeight_2017.dataHistoUp.Scale(1.0/pileupWeight_2017.dataHistoUp.Integral())
pileupWeight_2017.dataHistoDown.Scale(1.0/pileupWeight_2017.dataHistoDown.Integral())
pileupWeight_2017.CalculateWeight = calculatePileupWeight
pileupWeight_2017.hasUpDownUncertainties = True
pileupWeight_2017.uncertaintyVariationList = [
    "pileupWeight_UP",
    "pileupWeight_DOWN"
    ]
pileupWeight_2017.InitUncertaintyVariations()
pileupWeight_2017.uncertaintyVariationFunctions = {
    "pileupWeight_UP":calculatePileupWeight_Up,
    "pileupWeight_DOWN":calculatePileupWeight_Down
}

pileupWeight_2018 = Weight()
pileupWeight_2018.name = 'pileupWeighting'
pileupWeight_2018.mcHistoFilePath = b2gWeightPath+'mcPileupUL2018.root'
pileupWeight_2018.mcHistoFile = ROOT.TFile(pileupWeight_2018.mcHistoFilePath)
pileupWeight_2018.mcHisto = pileupWeight_2018.mcHistoFile.Get('pu_mc')
pileupWeight_2018.dataHistoFilePath = b2gWeightPath+'PileupHistogram-UL2018-100bins_withVar.root'
pileupWeight_2018.dataHistoFile = ROOT.TFile(pileupWeight_2018.dataHistoFilePath)
pileupWeight_2018.dataHisto = pileupWeight_2018.dataHistoFile.Get('pileup')
pileupWeight_2018.dataHistoUp = pileupWeight_2018.dataHistoFile.Get('pileup_plus')
pileupWeight_2018.dataHistoDown = pileupWeight_2018.dataHistoFile.Get('pileup_minus')
pileupWeight_2018.mcHisto.Scale(1.0/pileupWeight_2018.mcHisto.Integral())
pileupWeight_2018.dataHisto.Scale(1.0/pileupWeight_2018.dataHisto.Integral())
pileupWeight_2018.dataHistoUp.Scale(1.0/pileupWeight_2018.dataHistoUp.Integral())
pileupWeight_2018.dataHistoDown.Scale(1.0/pileupWeight_2018.dataHistoDown.Integral())
pileupWeight_2018.CalculateWeight = calculatePileupWeight
pileupWeight_2018.hasUpDownUncertainties = True
pileupWeight_2018.uncertaintyVariationList = [
    "pileupWeight_UP",
    "pileupWeight_DOWN"
    ]
pileupWeight_2018.InitUncertaintyVariations()
pileupWeight_2018.uncertaintyVariationFunctions = {
    "pileupWeight_UP":calculatePileupWeight_Up,
    "pileupWeight_DOWN":calculatePileupWeight_Down
}
