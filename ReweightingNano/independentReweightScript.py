#!/usr/bin/python3
import ROOT
import sys
from Utilities.RecursiveLoader import RecursiveLoader
import argparse
import traceback
from Configurations.ConfigDefinition import ReweightConfiguration
from array import array
from tqdm import tqdm
import Utilities.BranchRemovalTool as branchRemovalTool
from configDefaultPass import *

#*******IMPORTANT-NOTE***********
#When we want to add a new weight, we need to first remove all the old weights and the associated branches (using --Remove option) - this will prevent the creation of duplicate branches which 
# is a pain - as it gives erroneous weights
# This also means that - each time a  new 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Handle script for performing final reweighting of events')
    parser.add_argument('--ConfigFiles',nargs = '+',help="Python based config files used to specify samples",default=configList)
    parser.add_argument('--Remove',help = "Provide the recipe to remove the branches from the file, and then exit", action="store_true")
    parser.add_argument('--Channel',help = "Based on this option, the location of the input files will be changed", required=True,choices=['tt', 'et', 'mt','original'])
    args = parser.parse_args()
    theLoader= RecursiveLoader()    
    numErrors = 0
    for configFile in args.ConfigFiles:
        try:
            #first let's go and open the file and get our tree.
            print("Loading from configFile: "+configFile)
            theConfigModule = theLoader.LoadFromDirectoryPath(configFile)
            for item in dir(theConfigModule):
                theConfig = getattr(theConfigModule,item)
                if isinstance(theConfig,ReweightConfiguration):
                    break                        
            if(args.Remove):
                #okay, let's figure out the name of any branches we're going add.
                branchesToAdd=[]
                for weight in theConfig.listOfWeights:                
                    branchesToAdd.append(weight.name)
                    if weight.hasUpDownUncertainties:
                        for uncertainty in weight.uncertaintyVariationList:
                            branchesToAdd.append(uncertainty)
                branchesToAdd.append("FinalWeighting")
                for weight in theConfig.listOfWeights:
                    if weight.hasUpDownUncertainties:
                        for uncertainty in weight.uncertaintyVariationList:
                            branchesToAdd.append('FinalWeighting_'+uncertainty)                        
                #this is now deprecated with the creation of the branch removal tool
                """
                print("Removal Recipe: \'\n")
                theRecipe = "python PruneBranch.py --Branches "
                for branch in branchesToAdd:
                    theRecipe += branch+' '
                theRecipe += '--Files '
                print(theRecipe)
                print("\n\'")
                """
                if args.Channel == "tt":
                    branchRemovalTool.PruneBranches(theConfig.inputFile_tt,branchesToAdd)
                if args.Channel == "et":
                    branchRemovalTool.PruneBranches(theConfig.inputFile_et,branchesToAdd)
                if args.Channel == "mt":
                    branchRemovalTool.PruneBranches(theConfig.inputFile_mt,branchesToAdd)
                if args.Channel == "original":
                    branchRemovalTool.PruneBranches(theConfig.inputFile,branchesToAdd)
                
                continue

            #now get on with it
            #Here we will add the condtion to process different files based on the channel selection

            if args.Channel == "tt":
                theFile = ROOT.TFile.Open(theConfig.inputFile_tt,"UPDATE")
            if args.Channel == "et":
                theFile = ROOT.TFile.Open(theConfig.inputFile_et,"UPDATE")
            if args.Channel == "mt":
                theFile = ROOT.TFile.Open(theConfig.inputFile_mt,"UPDATE")
            if args.Channel == "original":
                theFile = ROOT.TFile.Open(theConfig.inputFile,"UPDATE")

            #theFile = ROOT.TFile.Open(theConfig.inputFile,"UPDATE")
            theTree = theFile.Events
            print("Creating individual event weights...")                        
            weightsBranchesDictionary = {}
            weightsVariationBranchesDictionary = {}
            for weight in theConfig.listOfWeights:
                weightsBranchesDictionary[weight.name]=theTree.Branch(weight.name,weight.value,weight.name+'/F')
                if weight.hasUpDownUncertainties:
                    for uncertainty in weight.uncertaintyVariationList:
                        weightsVariationBranchesDictionary[uncertainty] = theTree.Branch(uncertainty,weight.uncertaintyVariationArrays[uncertainty],uncertainty+'/F')
            print("Creating final weights...")
            #Let's create a final weighting branch
            theFinalWeight = array('f',[0.])
            theFinalWeightBranch = theTree.Branch("FinalWeighting",theFinalWeight,"FinalWeighting/F")
            #figure out how many configurations we have that have up and down uncertainties.
            #if they have them, let's create final branches to account for that.
            finalWeightVariations = {}
            finalWeightVariationsBranches = {}
            for weight in theConfig.listOfWeights:
                if weight.hasUpDownUncertainties:
                    for uncertainty in weight.uncertaintyVariationList:
                        uncertaintyName = 'FinalWeighting_'+uncertainty
                        finalWeightVariations[uncertaintyName] = array('f',[0.])
                        finalWeightVariationsBranches[uncertaintyName] = theTree.Branch(uncertaintyName,finalWeightVariations[uncertaintyName],uncertaintyName+'/F')
            #Now let's loop the tree
            print("Looping over the tree...")
            for i in tqdm(range(theTree.GetEntries())):
                theTree.GetEntry(i)
                #...this could be coded better. Little redundant.
                #create final weightings
                #set things to defaults.
                #default to one, for things like data and embedded                
                theFinalWeight[0] = 1.0
                for weight in theConfig.listOfWeights:
                    if weight.hasUpDownUncertainties:
                        for uncertainty in weight.uncertaintyVariationList:
                            uncertaintyName = 'FinalWeighting_'+uncertainty
                            finalWeightVariations[uncertaintyName][0] = 1.0                            
                #okay, let's loop over each weight
                print ("Beginning of the Event")
                for weight in theConfig.listOfWeights:
                    #calculate the nominal value                    
                    weight.CalculateWeight(weight,theTree)
                    #if it has an up down uncertainty let's calculate that too.
                    if weight.hasUpDownUncertainties:
                        for uncertainty in weight.uncertaintyVariationList:
                            weight.uncertaintyVariationFunctions[uncertainty](weight,theTree,uncertainty)                            
                    #the nominal final weight is a product of all available nominal weights
                    print ("Final Weight in stages:",theFinalWeight[0],weight.value[0])
                    theFinalWeight[0] = theFinalWeight[0] * weight.value[0]
                    print ("Multiplied weight:",theFinalWeight[0])
                    #if this weight has an up/down uncertainty, let's find it's branch and get it properly modified
                    if weight.hasUpDownUncertainties:
                        for uncertainty in weight.uncertaintyVariationList:
                            uncertaintyName = 'FinalWeighting_'+uncertainty                                                        
                            finalWeightVariations[uncertaintyName][0] = finalWeightVariations[uncertaintyName][0] * weight.uncertaintyVariationArrays[uncertainty][0]
                            #stuff is zero here
                    #find everything that isn't this weight's up down uncertainties
                    #and make sure it is modified with the nominal
                    #how do we do this?
                    #let's make a list of all the already handled variations
                    #stuff is zero here
                    alreadyHandledVariations = []
                    for uncertainty in weight.uncertaintyVariationList:
                        uncertaintyName = 'FinalWeighting_'+uncertainty
                        alreadyHandledVariations.append(uncertaintyName)
                    for key in finalWeightVariations:                        
                        if key not in alreadyHandledVariations:
                            finalWeightVariations[key][0] = finalWeightVariations[key][0] * weight.value[0]
                #debug print statement
                #print ""
                #print "Event #"+str(i+1)
                #for weight in theConfig.listOfWeights:
                #    print(weight.name+": "+str(weight.value[0]))
                #print("FinalWeighting: "+str(theFinalWeight[0]))
                #fill everything
                for branch in weightsBranchesDictionary:
                    weightsBranchesDictionary[branch].Fill()
                for branch in weightsVariationBranchesDictionary:
                    weightsVariationBranchesDictionary[branch].Fill()
                theFinalWeightBranch.Fill()
                for branch in finalWeightVariationsBranches:                    
                    finalWeightVariationsBranches[branch].Fill()
        except Exception as error:
            print("Error! Details:")
            traceback.print_exc()
            numErrors+=1
        else:
            print("Finished up. Writing...")
            theTree.Write("",ROOT.TObject.kOverwrite)
            theFile.Write()
            theFile.Close()
            del theConfig
    if(numErrors > 0):
        print("There were "+str(numErrors)+" errors(s).")
        print("Please check them.")
    else:
        print("Completed with no errors!")
        