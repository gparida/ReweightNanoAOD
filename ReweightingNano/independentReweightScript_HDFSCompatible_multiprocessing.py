#!/usr/bin/env python3
import ROOT
import os
import sys
from Utilities.RecursiveLoader import RecursiveLoader
import argparse
import traceback
from Configurations.ConfigDefinition import ReweightConfiguration
from array import array
from tqdm import tqdm
#import Utilities.BranchRemovalTool as branchRemovalTool
import Utilities.BranchRemovalTool_Ganesh as branchRemovalTool
#from configDefaultPass_2016 import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
import multiprocessing as  np
from treeReaderArrayTools import InputTree

  


    
def reweight_multiprocessing(configFile):    
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
            
            #continue
            return 0
        #now get on with it
        #Here we will add the condtion to process different files based on the channel selection
        #This section is written because currently I donot know how to write files to hdfs directly
        #We need to create temporary file in scratch, perfrom the entire weighting and then transfer it back to hdfs
        if args.Channel == "original":
            theOriginalFile = ROOT.TFile.Open(theConfig.inputFile,"READ")
        #create a new file in the scratch area            
        #newFileName = "/nfs_scratch/parida/ReweightFilesTempStore/"+"file_temporary.root"
        #newFileName ="/nfs_scratch/parida/ReweightFilesTempStore/"+theConfig.inputFile[:theConfig.inputFile.index(".root")].split("/")[-1] + "_temporary.root"
        newFileName = args.tempStore+"/"+theConfig.inputFile[:theConfig.inputFile.index(".root")].split("/")[-1] + "_temporary.root"
        print ("Temporary File location and name = ",newFileName)
        
        #Open the new file
        newFile = ROOT.TFile(newFileName,"RECREATE")
        alreadyGrabbedItems = []
        for keyObj in theOriginalFile.GetListOfKeys():
            if keyObj.GetName() not in alreadyGrabbedItems:
                obj = theOriginalFile.Get(keyObj.GetName())
                newFile.cd()
                if type(obj) == type(ROOT.TTree()):
                    obj = obj.CloneTree(-1,"fast")
                obj.Write()
                alreadyGrabbedItems.append(keyObj.GetName())
        newFile.Write()
        print ("Closing the temporary file...Original file close statement gives an error statement")
        newFile.Close()
        #theOriginalFile.Close()
        #now we start
        print ("Continue to add new branches to the new file")
        theFile = ROOT.TFile.Open(newFileName,"UPDATE")
        #if args.Channel == "tt":
        #    theFile = ROOT.TFile.Open(theConfig.inputFile_tt,"UPDATE")
        #if args.Channel == "et":
        #    theFile = ROOT.TFile.Open(theConfig.inputFile_et,"UPDATE")
        #if args.Channel == "mt":
        #    theFile = ROOT.TFile.Open(theConfig.inputFile_mt,"UPDATE")
        #if args.Channel == "original":
        #    theFile = ROOT.TFile.Open(theConfig.inputFile,"UPDATE")
        #theFile = ROOT.TFile.Open(theConfig.inputFile,"UPDATE")
        theTree = theFile.Get("Events")
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
            #print ("Beginning of the Event")
            for weight in theConfig.listOfWeights:
                #calculate the nominal value                    
                weight.CalculateWeight(weight,theTree)
                #if it has an up down uncertainty let's calculate that too.
                if weight.hasUpDownUncertainties:
                    for uncertainty in weight.uncertaintyVariationList:
                        weight.uncertaintyVariationFunctions[uncertainty](weight,theTree,uncertainty)                            
                #the nominal final weight is a product of all available nominal weights
                #print ("Final Weight in stages:",theFinalWeight[0],weight.value[0])
                theFinalWeight[0] = theFinalWeight[0] * weight.value[0]
               #print ("Multiplied weight:",theFinalWeight[0])
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
        print("Now we move the temporary file back to the original location")
        #os.system("mv "+newFileName+" "+theConfig.inputFile)
        #os.system("hadoop fs -put -f "+newFileName+" "+theConfig.inputFile)
        os.system("hadoop fs -moveFromLocal -f "+newFileName+" "+theConfig.inputFile[theConfig.inputFile.index("/store"):])
        del theConfig

#*******IMPORTANT-NOTE***********
#When we want to add a new weight, we need to first remove all the old weights and the associated branches (using --Remove option) - this will prevent the creation of duplicate branches which 
# is a pain - as it gives erroneous weights
# This also means that - each time a  new 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Handle script for performing final reweighting of events')
    parser.add_argument('--ConfigFiles','-c',nargs = '+',help="Python based config files used to specify samples")
    parser.add_argument('--Remove',help = "Provide the recipe to remove the branches from the file, and then exit", action="store_true")
    parser.add_argument('--Channel',help = "Based on this option, the location of the input files will be changed", required=True,choices=['tt', 'et', 'mt','original'])
    parser.add_argument('--ncores','-n',help="Number of cores to be used for hadd",required=True)
    parser.add_argument('--year','-y',help="Specify the year. This is used to selection which default config to used.",choices=['2016APV', '2016', '2017','2018'],required=True)
    parser.add_argument('--tempStore','-t',help='Temporary staging area for files before moving out to hdfs', required=True)
    args = parser.parse_args()
    theLoader= RecursiveLoader()    
    numErrors = 0
    if (args.year=="2016APV"):
        print ("Importing the 2016APV default config file")
        from configDefaultPass_2016APV import *
    elif (args.year=="2016"):
        print ("Importing the 2016 default config file")
        from configDefaultPass_2016 import *
    elif (args.year=="2017"):
        print ("Importing the 2017 default config file")
        from configDefaultPass_2017 import *
    elif (args.year=="2018"):
        print ("Importing the 2018 default config file")
        from configDefaultPass_2018 import *  

    if (args.ConfigFiles is not None):
        configList = [configs for configs in args.ConfigFiles]
        print (configList)

    pool = np.Pool(int(args.ncores))
    res=pool.map(reweight_multiprocessing,configList)

    print("Total number of errors = ",numErrors)

        
