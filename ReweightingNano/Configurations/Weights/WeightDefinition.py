#!/usr/bin/python3
#this class will be our interface for defining a weight and how to get at it.
import ROOT
from array import array

class Weight():
    def __init__(self):
        self.name = ''
        self.hasUpDownUncertainties = False
        self.value = array('f',[0])
        self.upValue = array('f',[0])
        self.downValue = array('f',[0])        
        self.uncertaintyVariationList = []
        self.uncertaintyVariationArrays = {}
        self.uncertaintyVariationFunctions = {}    
    #calculate the weight necessary, given information in the tree
    #this will need to be defined by whichever module is using this at the time.
    def CalculateWeight(self,theTree):
        raise RuntimeError("Default CalculateWeight()! Please define a way to calculate weights!")
    def DefaultVariationFunction(self,theTree):
        raise RuntimeError("Default Variation Function! please define a function for how to handle this error on the weight!")
    def InitUncertaintyVariations(self):
        for uncertainty in self.uncertaintyVariationList:
            self.uncertaintyVariationArrays[uncertainty] = array('f',[0.])