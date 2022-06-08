import ROOT
import .Weights.WeightDefinition 

class ReweightConfiguration():
    def __init__(self):
        self.name = ''
        self.inputFile=''
        self.inputFile_tt=''
        self.inputFile_et=''
        self.inputFile_mt=''
        self.listOfWeights=[]