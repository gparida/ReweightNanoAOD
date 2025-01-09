import time
import os
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import json
import glob
import numpy as np
from re import search
import multiprocessing as  mp
import argparse
import math
import os 

class theorySystematics(Module):
	def __init__(self, filename, year=2016, isData=False,runNominal=False):
		self.runNominal = runNominal
		print("ACTIVATE: WeightsAndAssociatedSystematics")
		self.year = year
		if ((self.year =="2016APV") or (self.year =="2016")):
			self.year_unc = "2016"
		elif ((self.year =="2017") or (self.year =="2018")):
			self.year_unc = year
		self.isMC =  not isData
		self.isData = isData
		self.filename = filename
		self.branches = ["isrUp", "isrDown", "fsrUp", "fsrDown", "pdfUp", "pdfDown", "qcdscalerenormUp", "qcdscalerenormDown","qcdscalefactoUp", "qcdscalefactoDown"]



	def beginJob(self):
		pass


	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		#Modify the code to input the XS weights calculation
		self.out = wrappedOutputTree
		if (self.isMC):
			for branch in self.branches:
				self.out.branch(branch, "F")  # F for float branches
		
		#Nothing to do for Data sinc we are not rejecting events


	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass

	def analyze(self, event):
		if self.isData:
			#Nothing to do
			return True
		# Initialize default weights
		#isr = {"nominal": 1.0, "up": 1.0, "down": 1.0}
		#fsr = {"nominal": 1.0, "up": 1.0, "down": 1.0}
		pdf = {"nominal": 1.0, "up": 1.0, "down": 1.0}
		qcdscale = {
			"renorm_up": 1.0, "renorm_down": 1.0,
			"fact_up": 1.0, "fact_down": 1.0,
		}
		# Access event-level weights and collections
		#PSWeight = getattr(event, "PSWeight", None)
		#LHEPdfWeight = getattr(event, "LHEPdfWeight", None)
		#LHEScaleWeight = getattr(event, "LHEScaleWeight", None)

		#PSWeight = Collection(event, "PSWeight", "nPSWeight")
		#LHEPdfWeight = Collection(event, "LHEPdfWeight", "nLHEPdfWeight")
		#LHEScaleWeight = Collection(event, "LHEScaleWeight", "nLHEScaleWeight")	

		#Generator = getattr(event, "Generator", None)
		#LHEWeight = getattr(event, "LHEWeight", None)

		# PDF uncertainty weights
		#print ("Size of LHEPdfWeight",event.nLHEPdfWeight,event.LHEPdfWeight)
		#if LHEPdfWeight is not None and len(event.LHEPdfWeight) > 0:
		if event.nLHEPdfWeight > 0:
			LHEPdfWeight_0 = event.LHEPdfWeight[0] if event.LHEPdfWeight[0] != 0 else 1.0
			#print("LHEPdfWeight _ 0",LHEPdfWeight_0)
			LHEPdfVariation = [(w / LHEPdfWeight_0) for w in event.LHEPdfWeight]
			#print("\n\n\n\n\n\n PDF up variation = ",max(LHEPdfVariation)," PDF dwon variation = ", min(LHEPdfVariation))
			pdf = {
				"nominal": 1.0,
				"up": max(LHEPdfVariation),
				"down": min(LHEPdfVariation),
			}
		
		# ISR / FSR uncertainty weights
		#I currently donot have Generator_* branches
		##if PSWeight is not None and Generator and LHEWeight:
		##	if Generator.weight != LHEWeight.originalXWGTUP:
		##		psWeights = (
		##			np.array(PSWeight)
		##			* LHEWeight.originalXWGTUP
		##			/ Generator.weight
		##		)
		##	else:
		#psWeights = np.array(PSWeight)
		PSWeightISRUp = PSWeightISRDown = PSWeightFSRUp = PSWeightFSRDown = 1
		if event.nPSWeight == 4:
			PSWeightISRUp = event.PSWeight[2]
			PSWeightISRDown = event.PSWeight[0]
			PSWeightFSRUp = event.PSWeight[3]
			PSWeightFSRDown = event.PSWeight[1]

		##isr = {
		##	"nominal": 1.0,
		##	"up": psWeights[2] if len(psWeights) > 2 else 1.0,
		##	"down": psWeights[0] if len(psWeights) > 0 else 1.0,
		##}
		##fsr = {
		##	"nominal": 1.0,
		##	"up": psWeights[3] if len(psWeights) > 3 else 1.0,
		##	"down": psWeights[1] if len(psWeights) > 1 else 1.0,
		##}

		# LHEScale weights
		#if LHEScaleWeight is not None and LHEScaleWeight.GetSize() == 9:
		if event.nLHEScaleWeight == 9:
			qcdscale = {
				"renorm_up": event.LHEScaleWeight[7],
				"renorm_down": event.LHEScaleWeight[1],
				"fact_up": event.LHEScaleWeight[5],
				"fact_down": event.LHEScaleWeight[3],
			}
		
		#print("\n\n renorm_up = ",qcdscale["renorm_up"]," renorm_down = ", qcdscale["renorm_down"])
		#print("\n\n fact_up = ",qcdscale["fact_up"]," fact_down = ", qcdscale["fact_down"])
		#print("\n\n isrUp = ",PSWeightISRUp," isrDown = ", PSWeightISRDown)
		#print("\n\n fsrUp = ",PSWeightFSRUp," fsrDown = ", PSWeightFSRDown)
		# Write weights to output branches
		self.out.fillBranch("isrUp", PSWeightISRUp)
		self.out.fillBranch("isrDown", PSWeightISRDown)
		self.out.fillBranch("fsrUp", PSWeightFSRUp)
		self.out.fillBranch("fsrDown", PSWeightFSRDown)
		self.out.fillBranch("pdfUp", pdf["up"])
		self.out.fillBranch("pdfDown", pdf["down"])
		self.out.fillBranch("qcdscalerenormUp", qcdscale["renorm_up"])
		self.out.fillBranch("qcdscalerenormDown", qcdscale["renorm_down"])
		self.out.fillBranch("qcdscalefactoUp", qcdscale["fact_up"])
		self.out.fillBranch("qcdscalefactoDown", qcdscale["fact_down"])

		return True        


class JetMassCorrections(Module):
	def __init__(self, filename, year=2016, isData=False,runNominal=False):
		self.runNominal = runNominal
		print("ACTIVATE: WeightsAndAssociatedSystematics")
		self.year = year
		if ((self.year =="2016APV") or (self.year =="2016")):
			self.year_unc = "2016"
		elif ((self.year =="2017") or (self.year =="2018")):
			self.year_unc = year
		self.isMC =  not isData
		self.isData = isData
		self.filename = filename
		# Define JMS and JMR factors for different eras
		self.jms_factors = {
			"2016APV": {"central": 0.985, "up": 1.000, "down": 0.970},
			"2016": {"central": 0.988, "up": 1.000, "down": 0.976},
			"2017": {"central": 0.994, "up": 1.000, "down": 0.989},
			"2018": {"central": 0.998, "up": 1.003, "down": 0.993},
		}
		self.jmr_factors = {
			"2016APV": {"central": 1.013, "up": 1.043, "down": 0.000},
			"2016": {"central": 1.015, "up": 1.045, "down": 0.000},
			"2017": {"central": 1.009, "up": 1.039, "down": 0.000},
			"2018": {"central": 1.010, "up": 1.040, "down": 0.000},
		}

		if ((self.isData) or (self.runNominal)):
			self.jesUnc = [""]
		else:
			self.jesUnc = ["jesTotalUp","jesTotalDown","jerUp","jerDown",
						   "jesAbsoluteUp","jesAbsoluteDown",
						   "jesAbsolute_%sUp"%(self.year_unc),"jesAbsolute_%sDown"%(self.year_unc),
						   "jesBBEC1Up", "jesBBEC1Down",
						   "jesBBEC1_%sUp"%(self.year_unc),"jesBBEC1_%sDown"%(self.year_unc),
						   "jesEC2Up","jesEC2Down",
						   "jesEC2_%sUp"%(self.year_unc),"jesEC2_%sDown"%(self.year_unc),
						   "jesFlavorQCDUp","jesFlavorQCDDown",
						   "jesHFUp","jesHFDown",
						   "jesHF_%sUp"%(self.year_unc), "jesHF_%sDown"%(self.year_unc),
						   "jesRelativeBalUp","jesRelativeBalDown",
						   "jesRelativeSample_%sUp"%(self.year_unc),"jesRelativeSample_%sDown"%(self.year_unc),
						   "UnclustUp","UnclustDown"]
	def beginJob(self):
		pass

	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		# Output branches
		if (self.isMC):
			self.out.branch("pnetmassnom", "F")
			self.out.branch("pnetmassjmrUp", "F")
			self.out.branch("pnetmassjmrDown", "F")
			self.out.branch("pnetmassjmsUp", "F")
			self.out.branch("pnetmassjmsDown", "F")
			#--->>Here we need separate nominal branches for the jet and the met variations
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("pnetmassnom%s"%(sys),"F")
		elif (self.isData):
			self.out.branch("pnetmassnom", "F")



	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass

	def analyze(self, event):
		# Access pnetmass branch
		pnetmass = getattr(event, "pnetmass")
		if pnetmass < 0:  # Skip invalid entries
			self.out.fillBranch("pnetmassnom", -1.00)
			if (self.isMC):
				self.out.fillBranch("pnetmassjmrUp", -1.00)
				self.out.fillBranch("pnetmassjmrDown", -1.00)
				self.out.fillBranch("pnetmassjmsUp", -1.00)
				self.out.fillBranch("pnetmassjmsDown", -1.00)
			return True

		# Retrieve JMS and JMR factors for the current era
		jms = self.jms_factors[self.year]
		jmr = self.jmr_factors[self.year]

		# Gaussian smearing RMS
		sigma = 1.0  # RMS of the normal distribution
		smear_factor_central = np.sqrt(pow(1.01 * sigma, 2) - pow(sigma, 2))
		smear_factor_up = np.sqrt(pow(jmr["up"] * sigma, 2) - pow(sigma, 2))
		smear_factor_down = np.sqrt(pow(jmr["down"] * sigma, 2) - pow(sigma, 2)) if jmr["down"] > 0 else 0


		# Corrected masses
		if (self.isMC):
			pnetmassnom = (pnetmass * jms["central"]) + np.random.normal(0, smear_factor_central)
			pnetmass_jmrup = (pnetmass * jms["central"]) + np.random.normal(0, smear_factor_up)
			pnetmass_jmrdown = (pnetmass * jms["central"]) + np.random.normal(0, smear_factor_down)
			pnetmass_jmsup = pnetmass * jms["up"]
			pnetmass_jmsdown = pnetmass * jms["down"]
		elif (self.isData):
			pnetmassnom = (pnetmass * jms["central"])

		# Fill output branches
		self.out.fillBranch("pnetmassnom", pnetmassnom)
		if(self.isMC):
			self.out.fillBranch("pnetmassjmrUp", pnetmass_jmrup)
			self.out.fillBranch("pnetmassjmrDown", pnetmass_jmrdown)
			self.out.fillBranch("pnetmassjmsUp", pnetmass_jmsup)
			self.out.fillBranch("pnetmassjmsDown", pnetmass_jmsdown)

			# Handle systematic branches
			for sys in self.jesUnc:  # Replace with actual systematic list
				branch_name = f"pnetmass{sys}"
				#if hasattr(event, branch_name):
				pnetmass_sys = getattr(event, branch_name)
				if pnetmass_sys >= 0:
					pnetmassnom_sys = (pnetmass_sys * jms["central"]) + np.random.normal(0, smear_factor_central)
					self.out.fillBranch("pnetmassnom%s"%(sys), pnetmassnom_sys)
				else:
					self.out.fillBranch("pnetmassnom%s"%(sys), -1.0)

		return True


def call_postpoc(files):
	nameStrip=files.strip()
	filename = (nameStrip.split('/')[-1]).split('.')[-2]
	print(filename)
	
	if (search("Run", filename)):
		print ("This is a ",args.year," Data file = ",filename)
		theorySys = lambda: theorySystematics(filename,args.year,True,args.runNominal)
		jetmassSys = lambda: JetMassCorrections(filename,args.year,True,args.runNominal)
	else:
		print ("This is a ",args.year," MC file = ", filename)
		theorySys = lambda: theorySystematics(filename,args.year,False,args.runNominal)
		jetmassSys = lambda: JetMassCorrections(filename,args.year,False,args.runNominal)
	
	p = PostProcessor(args.tempStore,[files], cut=None, branchsel=None,modules=[theorySys(),jetmassSys()], postfix="",noOut=False,outputbranchsel=None)
	p.run()
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)	
	print("###############MOVING THE OUTPUT FILE BACK TO HDFS#######################")
	#os.system("hadoop fs -moveFromLocal -f "+args.tempStore+"/"+filename+".root"+" "+outputDir+"/.") #This currently doesnot work due to username differences - it takes parida by default
	os.system("mv " + args.tempStore + "/" + filename + ".root " + outputDir + "/.")
	print("Moved the ROOT file to output directory.")

if __name__ == "__main__":
	start_time = time.time()
	parser = argparse.ArgumentParser(description='Add W and Z genpt weight')	
	parser.add_argument('--inputLocation','-i',help="enter the path to the location of input file set",default="")
	parser.add_argument('--outputLocation','-o',help="enter the path where you want the output files to be stored",default =".")
	parser.add_argument('--ncores','-n',help ="number of cores for parallel processing", default=1)
	parser.add_argument('--year','-y',help='specify the run - to make sure right triggers are used',choices=['2016','2016APV','2017','2018'])
	parser.add_argument('--tempStore','-t',help='Temporary staging area for files before moving out to hdfs', required=True)
	parser.add_argument('--runNominal','-rnom',help='Run the script without the systematic variations',action='store_true')

	args = parser.parse_args()

	#fnames = list(set(glob.glob(args.inputLocation + "/*.root"))-set(glob.glob(args.inputLocation + "/*MET*Run*.root"))) #making a list of input MC/DATA files
	#Run the module for only MC files:
	#fnames = list(set(glob.glob(args.inputLocation + "/*.root"))-set(glob.glob(args.inputLocation + "/*SingleMu_*.root"))-set(glob.glob(args.inputLocation + "/*MET*.root")))
	fnames = glob.glob(args.inputLocation + "/*.root")

	print("\n\n\n>>>>List of files processing\n")
	print ([(nameStrip.strip().split('/')[-1]).split('.')[-2] for nameStrip in fnames])
	print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	#exit()
	#fnames = glob.glob(args.inputLocation + "/*Radion*1000*.root")
	outputDir = args.outputLocation

	argList = list()
	for file in fnames:
		argList.append(file)

	if int(args.ncores) == 1:
		for arr in argList:
			print ("Using a single thread ")
			call_postpoc(arr)
	
	else:
		try:
			print ("Using Multithreading")
			pool = mp.Pool(int(args.ncores))
			print ("list", argList)
			res=pool.map(call_postpoc, argList)
		except Exception as error:
			print ("MultiProc error - needs debugging")
			print("An exception occurred:", type(error).__name__)

	end_time = time.time()
	elapsed_time = end_time - start_time
	print("Elapsed Time: {:.2f} seconds".format(elapsed_time))
	elapsed_time_hours = elapsed_time / 3600  # Convert seconds to hours
	print("Elapsed Time: {:.2f} hours".format(elapsed_time_hours))