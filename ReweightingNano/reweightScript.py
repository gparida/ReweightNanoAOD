from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Utilities.RecursiveLoader import RecursiveLoader
from Configurations.ConfigDefinition import ReweightConfiguration
import argparse
import traceback
import sys
import glob
import ROOT
from array import array
from tqdm import tqdm
ROOT.PyConfig.IgnoreCommandLineOptions = True



class addingWeights(Module):
    def __init__(self,configModule,configObject,listOfBranchesToAdd,listOfBranchesWithVariationToAdd,finalWeightBranch):
        self.sampleModule = configModule
        self.configObject = configObject
        self.listOfBranchesToAdd = listOfBranchesToAdd
        self.listOfBranchesWithVariationToAdd = listOfBranchesWithVariationToAdd
        self.finalWeightBranch = finalWeightBranch

        print ("Has the module transferred correctly: ", self.sampleModule)
        print ("Has the instance of reweighting transferred correctly", self.configObject)
        # add any arguments needed after the self and set them here
        

    def beginJob(self):
        pass

    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree #--->Is this the name of output file
        self.theTree = inputTree
        for name in range(len(self.listOfBranchesToAdd)):
            self.out.branch(listOfBranchesToAdd[name],"F")
        for name in range(len(self.listOfBranchesWithVariationToAdd)):
            self.out.branch(listOfBranchesWithVariationToAdd[name],"F")
        self.out.branch(self.finalWeightBranch,"F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        theFinalWeight = 1.0
        for weight in self.configObject.listOfWeights:
            weight.CalculateWeight(weight,self.theTree)
            self.out.fillBranch(weight.name,weight.value[0])
            theFinalWeight= theFinalWeight*weight.value[0]
        self.out.fillBranch(self.finalWeightBranch,theFinalWeight)
        return True



addingWeightsConstr = lambda: addingWeights(theConfigModule,theConfig,listOfBranchesToAdd,listOfBranchesWithVariationToAdd,finalWeightBranch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Handle script for performing final reweighting of events')
    parser.add_argument('--ConfigFiles',nargs = '+',help="Python based config files used to specify samples",required=True)

    args = parser.parse_args()
    theLoader= RecursiveLoader()    
    numErrors = 0

    for configFile in args.ConfigFiles:
        try:
            print("Loading from configFile: "+configFile)
            theConfigModule = theLoader.LoadFromDirectoryPath(configFile)
            for item in dir(theConfigModule):
                theConfig = getattr(theConfigModule,item)
                if isinstance(theConfig,ReweightConfiguration):
                    break

            listOfBranchesToAdd=[]
            listOfBranchesWithVariationToAdd=[]
            for weight in theConfig.listOfWeights:
                listOfBranchesToAdd.append(weight.name)
                if weight.hasUpDownUncertainties:
                    for uncertainity in weight.uncertaintyVariationList:
                        listOfBranchesWithVariationToAdd.append(uncertainity)

            finalWeightBranch = "finalWeight" 
            fnames = [str(theConfig.inputFile)]
            print ("file Name:  ",fnames)
            outputDir="."
        #addingWeightsConstr = lambda: addingWeights(theConfigModule,theConfig,listOfBranchesToAdd,listOfBranchesWithVariationToAdd,finalWeightBranch)
            p = PostProcessor(outputDir,inputFiles=fnames,branchsel=None,modules=[addingWeightsConstr()], postfix="_CS_Gen_Weight_applied",noOut=False)
            p.run()

        except Exception as error:
            print("Error! Details:")
            traceback.print_exc()
            numErrors+=1


    if(numErrors > 0):
        print("There were "+str(numErrors)+" errors(s).")
        print("Please check them.")
    else:
        print("Completed with no errors!")




