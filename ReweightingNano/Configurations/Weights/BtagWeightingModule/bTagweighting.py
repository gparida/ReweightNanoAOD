import ROOT
import os 
from Configurations.Weights.WeightDefinition import Weight as Weight
import json


def calculatebtagWeight(self, theTree):
    btagWeighting = 1.0

    print ("fatjet_pt ",theTree.gFatJet_pt[0])

    if (theTree.gFatJet_pt[0] >= 200 and theTree.gFatJet_pt[0] < 250):
        btagWeighting = jsonInfo["200_250"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 250 and theTree.gFatJet_pt[0] < 300):
        btagWeighting = jsonInfo["250_300"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 300 and theTree.gFatJet_pt[0] < 350):
        btagWeighting = jsonInfo["300_350"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 350 and theTree.gFatJet_pt[0] < 400):
        btagWeighting = jsonInfo["350_400"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 400 and theTree.gFatJet_pt[0] < 450):
        btagWeighting = jsonInfo["400_450"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 450 and theTree.gFatJet_pt[0] < 500):
        btagWeighting = jsonInfo["450_500"]["nominal"]

    elif (theTree.gFatJet_pt[0] >= 500 and theTree.gFatJet_pt[0] < 600):
        btagWeighting = jsonInfo["500_600"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 600 and theTree.gFatJet_pt[0] < 700):
        btagWeighting = jsonInfo["600_700"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 700 and theTree.gFatJet_pt[0] < 800):
        btagWeighting = jsonInfo["700_800"]["nominal"]
    
    elif (theTree.gFatJet_pt[0] >= 800):
        btagWeighting = jsonInfo["800_Inf"]["nominal"]
    
    self.value[0] = btagWeighting


def calculatebtagWeight_Up(self, theTree, uncert):
    print ("Entering Btagging Up")
    btagWeighting_Up = 1.0
    
    if (theTree.gFatJet_pt[0] >= 200 and theTree.gFatJet_pt[0] < 250):
        btagWeighting_Up = jsonInfo["200_250"]["nominal"] + jsonInfo["200_250"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 250 and theTree.gFatJet_pt[0] < 300):
        btagWeighting_Up = jsonInfo["250_300"]["nominal"] + jsonInfo["250_300"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 300 and theTree.gFatJet_pt[0] < 350):
        btagWeighting_Up = jsonInfo["300_350"]["nominal"] + jsonInfo["300_350"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 350 and theTree.gFatJet_pt[0] < 400):
        btagWeighting_Up = jsonInfo["350_400"]["nominal"] + jsonInfo["350_400"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 400 and theTree.gFatJet_pt[0] < 450):
        btagWeighting_Up = jsonInfo["400_450"]["nominal"] + jsonInfo["400_450"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 450 and theTree.gFatJet_pt[0] < 500):
        btagWeighting_Up = jsonInfo["450_500"]["nominal"] + jsonInfo["450_500"]["up"]

    elif (theTree.gFatJet_pt[0] >= 500 and theTree.gFatJet_pt[0] < 600):
        btagWeighting_Up = jsonInfo["500_600"]["nominal"] + jsonInfo["500_600"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 600 and theTree.gFatJet_pt[0] < 700):
        btagWeighting_Up = jsonInfo["600_700"]["nominal"] + jsonInfo["600_700"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 700 and theTree.gFatJet_pt[0] < 800):
        btagWeighting_Up = jsonInfo["700_800"]["nominal"] + jsonInfo["700_800"]["up"]
    
    elif (theTree.gFatJet_pt[0] >= 800):
        btagWeighting_Up = jsonInfo["800_Inf"]["nominal"] + jsonInfo["800_Inf"]["up"]

    print ("the up value btag =",btagWeighting_Up)
    self.uncertaintyVariationArrays[uncert][0] = btagWeighting_Up

def calculatebtagWeight_Down(self, theTree, uncert):
    btagWeighting_Down = 1.0
    
    if (theTree.gFatJet_pt[0] >= 200 and theTree.gFatJet_pt[0] < 250):
        btagWeighting_Down = jsonInfo["200_250"]["nominal"] - jsonInfo["200_250"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 250 and theTree.gFatJet_pt[0] < 300):
        btagWeighting_Down = jsonInfo["250_300"]["nominal"] - jsonInfo["250_300"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 300 and theTree.gFatJet_pt[0] < 350):
        btagWeighting_Down = jsonInfo["300_350"]["nominal"] - jsonInfo["300_350"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 350 and theTree.gFatJet_pt[0] < 400):
        btagWeighting_Down = jsonInfo["350_400"]["nominal"] - jsonInfo["350_400"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 400 and theTree.gFatJet_pt[0] < 450):
        btagWeighting_Down = jsonInfo["400_450"]["nominal"] - jsonInfo["400_450"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 450 and theTree.gFatJet_pt[0] < 500):
        btagWeighting_Down = jsonInfo["450_500"]["nominal"] - jsonInfo["450_500"]["down"]

    elif (theTree.gFatJet_pt[0] >= 500 and theTree.gFatJet_pt[0] < 600):
        btagWeighting_Down = jsonInfo["500_600"]["nominal"] - jsonInfo["500_600"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 600 and theTree.gFatJet_pt[0] < 700):
        btagWeighting_Down = jsonInfo["600_700"]["nominal"] - jsonInfo["600_700"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 700 and theTree.gFatJet_pt[0] < 800):
        btagWeighting_Down = jsonInfo["700_800"]["nominal"] - jsonInfo["700_800"]["down"]
    
    elif (theTree.gFatJet_pt[0] >= 800):
        btagWeighting_Down = jsonInfo["800_Inf"]["nominal"] - jsonInfo["800_Inf"]["down"]


    self.uncertaintyVariationArrays[uncert][0] = btagWeighting_Down  

    



btagWeight_2016 = Weight()
btagWeight_2016.name = 'btagWeighting'
btagWeight_2016.jsonSFFilePath = os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/ReweightingNano/Configurations/Weights/BtagWeightingModule/2016SF.json' 
#btagWeight_2016.jsonSFFile = '2016SF.json'
with open(btagWeight_2016.jsonSFFilePath,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
btagWeight_2016.CalculateWeight = calculatebtagWeight
btagWeight_2016.hasUpDownUncertainties = True
btagWeight_2016.uncertaintyVariationList = [
    "btagWeight_UP",
    "btagWeight_DOWN"
    ]
btagWeight_2016.InitUncertaintyVariations()
btagWeight_2016.uncertaintyVariationFunctions = {
    "btagWeight_UP":calculatebtagWeight_Up,
    "btagWeight_DOWN":calculatebtagWeight_Down
}





