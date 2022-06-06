import ROOT
from Weights.WeightDefinition import *

class ReweightConfiguration():
    def __init__(self):
        self.name = ''
        self.inputFile=''
        self.inputFile_tt=''
        self.inputFile_et=''
        self.inputFile_mt=''
        self.listOfWeights=[]