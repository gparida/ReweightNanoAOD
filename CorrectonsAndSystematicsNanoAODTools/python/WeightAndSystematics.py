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
from ReweightNanoAOD.CorrectonsAndSystematicsNanoAODTools.CorrectionHelpers.ak4btagging.btagJSONtool import *
from ReweightNanoAOD.CorrectonsAndSystematicsNanoAODTools.CorrectionHelpers.WandZptWeight.kFactorTool import *
from correctionlib import _core
import os 

class WeightsAndAssociatedSystematics(Module):
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
		if self.year == '2016': #not fond of having the configuration spread out like this
			self.LHCLumi =  16.81e15
		elif self.year == '2016APV':
			self.LHCLumi = 19.52e15
		elif self.year == '2017':
			self.LHCLumi = 41.48e15
		elif self.year == '2018':
			self.LHCLumi = 59.83e15
		#self. jesUnc = ["","jesUp","jesDown","jerUp","jerDown","tesUp","tesDown"]
		self.kFactorTool = KFactorTool(year=self.year)

		#AK8 pnet thresholds
		if(self.year=="2016APV"):
			self.pnetloose = 0.9088
			self.pnetmedium = 0.9737
			self.pnettight = 0.9883
			#load the json file with weights
			self.jsonFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/CorrectonsAndSystematicsNanoAODTools/python/CorrectionHelpers/HbbpnetSFs/2016APV_weights.json'


		elif(self.year=="2016"):
			self.pnetloose = 0.9137
			self.pnetmedium = 0.9735
			self.pnettight = 0.9883
			self.jsonFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/CorrectonsAndSystematicsNanoAODTools/python/CorrectionHelpers/HbbpnetSFs/2016_weights.json'


		elif(self.year=="2017"):
			self.pnetloose = 0.9105
			self.pnetmedium = 0.9714
			self.pnettight = 0.9870
			self.jsonFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/CorrectonsAndSystematicsNanoAODTools/python/CorrectionHelpers/HbbpnetSFs/2017_weights.json'	

		elif(self.year=="2018"):
			self.pnetloose = 0.9172
			self.pnetmedium = 0.9734
			self.pnettight = 0.9880
			self.jsonFile = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/CorrectonsAndSystematicsNanoAODTools/python/CorrectionHelpers/HbbpnetSFs/2018_weights.json'

		print("Year = ",self.year," file = ",self.jsonFile)

		with open(self.jsonFile,'r') as jsonFileRead:
			self.jsonInfo = json.load(jsonFileRead) 	

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

		#For AK4 btagging weights
		if self.isMC:
			#self.btagTool_medium = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='central',year=self.year)
			#self.btagTool_tight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='central',year=self.year)

			self.btagTool =  BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='central',year=self.year)
			self.btagToolTight =  BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='central',year=self.year)

			#For heavy flavs
			#For heavy flavs-->Medium WPs
			self.btagToolbcUpCorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='up_correlated', sigmalight='central',year=self.year)
			self.btagToolbcDownCorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='down_correlated', sigmalight='central',year=self.year)
			self.btagToolbcUpUncorrelated =  BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='up_uncorrelated', sigmalight='central',year=self.year)
			self.btagToolbcDownUncorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='down_uncorrelated', sigmalight='central',year=self.year)

			#For heavy flavs-->Tight WPs
			self.btagToolbcUpCorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='up_correlated', sigmalight='central',year=self.year)
			self.btagToolbcDownCorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='down_correlated', sigmalight='central',year=self.year)
			self.btagToolbcUpUncorrelatedTight =  BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='up_uncorrelated', sigmalight='central',year=self.year)
			self.btagToolbcDownUncorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='down_uncorrelated', sigmalight='central',year=self.year)

			#For light flavs
			#For light flavs-->Medium WPs
			self.btagToollightUpCorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='up_correlated',year=self.year)
			self.btagToollightDownCorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='down_correlated',year=self.year)
			self.btagToollightUpUncorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='up_uncorrelated',year=self.year)
			self.btagToollightDownUncorrelated = BTagWeightTool(tagger="deepjetflavb",wp='medium', sigmabc='central', sigmalight='down_uncorrelated',year=self.year)

			#For light flavs-->Tight WPs
			self.btagToollightUpCorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='up_correlated',year=self.year)
			self.btagToollightDownCorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='down_correlated',year=self.year)
			self.btagToollightUpUncorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='up_uncorrelated',year=self.year)
			self.btagToollightDownUncorrelatedTight = BTagWeightTool(tagger="deepjetflavb",wp='tight', sigmabc='central', sigmalight='down_uncorrelated',year=self.year)


		#For pile up weights
		if self.year == "2016":
			self.evaluator_pileup = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/LUM/'+'2016postVFP_UL/puWeights.json.gz')["Collisions16_UltraLegacy_goldenJSON"]	
			self.evaluator_electronid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'+'2016postVFP_UL/electron.json.gz')["UL-Electron-ID-SF"]
			self.evaluator_muonid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2016postVFP_UL/muon_Z.json.gz')["NUM_LooseID_DEN_genTracks"]
			self.evaluator_muoniso = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2016postVFP_UL/muon_Z.json.gz')["NUM_LooseRelIso_DEN_LooseID"]
			self.evaluator_hpstauid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/TAU/'+'2016postVFP_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2016_postVFP.json.gz')["DeepTau2018v2p5VSjet"]					
			self.evaluator_rootfile = ROOT.TFile(os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/TriggerSF/'+'2016_MetTriggerSFs.root')
			self.evaluator_sfHistoDir = self.evaluator_rootfile.GetDirectory("SF")
			self.evaluator_sfHisto = self.evaluator_sfHistoDir.Get("MET_SF")
		elif self.year == "2016APV":
			self.evaluator_pileup =_core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/LUM/'+'2016preVFP_UL/puWeights.json.gz')["Collisions16_UltraLegacy_goldenJSON"]	
			self.evaluator_electronid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'+'2016preVFP_UL/electron.json.gz')["UL-Electron-ID-SF"]
			self.evaluator_muonid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2016preVFP_UL/muon_Z.json.gz')["NUM_LooseID_DEN_genTracks"]
			self.evaluator_muoniso = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2016preVFP_UL/muon_Z.json.gz')["NUM_LooseRelIso_DEN_LooseID"]		
			self.evaluator_hpstauid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/TAU/'+'2016preVFP_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2016_preVFP.json.gz')["DeepTau2018v2p5VSjet"]					
			self.evaluator_rootfile = ROOT.TFile(os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/TriggerSF/'+'2016APV_MetTriggerSFs.root')
			self.evaluator_sfHistoDir = self.evaluator_rootfile.GetDirectory("SF")
			self.evaluator_sfHisto = self.evaluator_sfHistoDir.Get("MET_SF")		
		elif self.year == "2017":
			self.evaluator_pileup =_core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/LUM/'+'2017_UL/puWeights.json.gz')["Collisions17_UltraLegacy_goldenJSON"]	
			self.evaluator_electronid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'+'2017_UL/electron.json.gz')["UL-Electron-ID-SF"]
			self.evaluator_muonid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2017_UL/muon_Z.json.gz')["NUM_LooseID_DEN_genTracks"]
			self.evaluator_muoniso = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2017_UL/muon_Z.json.gz')["NUM_LooseRelIso_DEN_LooseID"]
			self.evaluator_hpstauid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/TAU/'+'2017_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2017.json.gz')["DeepTau2018v2p5VSjet"]					
			self.evaluator_rootfile = ROOT.TFile(os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/TriggerSF/'+'2017_MetTriggerSFs.root')
			self.evaluator_sfHistoDir = self.evaluator_rootfile.GetDirectory("SF")
			self.evaluator_sfHisto = self.evaluator_sfHistoDir.Get("MET_SF")	
		elif self.year == "2018":
			self.evaluator_pileup =_core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/LUM/'+'2018_UL/puWeights.json.gz')["Collisions18_UltraLegacy_goldenJSON"]				
			self.evaluator_electronid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/EGM/'+'2018_UL/electron.json.gz')["UL-Electron-ID-SF"]
			self.evaluator_muonid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2018_UL/muon_Z.json.gz')["NUM_LooseID_DEN_genTracks"]
			self.evaluator_muoniso = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/MUO/'+'2018_UL/muon_Z.json.gz')["NUM_LooseRelIso_DEN_LooseID"]
			self.evaluator_hpstauid = _core.CorrectionSet.from_file(os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/TAU/'+'2018_UL/Deepv2p5/tau_DeepTau2018v2p5_UL2018.json.gz')["DeepTau2018v2p5VSjet"]					
			self.evaluator_rootfile = ROOT.TFile(os.environ['CMSSW_BASE'] + '/src/ReweightNanoAOD/MetaData/TriggerSF/'+'2018_MetTriggerSFs.root')
			self.evaluator_sfHistoDir = self.evaluator_rootfile.GetDirectory("SF")
			self.evaluator_sfHisto = self.evaluator_sfHistoDir.Get("MET_SF")		
	def beginJob(self):
		if self.isMC:
			self.xsJSON = os.environ['CMSSW_BASE']+"/src/ReweightNanoAOD/MetaData/%s_Samples.json"%(self.year) #Add a customization to different yrs
			with open(self.xsJSON,'r') as xsjson:
				self.xsInfo = json.load(xsjson)


			self.countsJSON = os.environ['CMSSW_BASE']+'/src/ReweightNanoAOD/MetaData/SumOfGenWeights/%s_weight.json'%(self.year) #Add a customization to different yrs
			with open(self.countsJSON,'r') as countsjson:
				self.countsInfo = json.load(countsjson)


	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		#Modify the code to input the XS weights calculation
		self.out = wrappedOutputTree
		if (self.isMC):
			print(" The inputFile name gotten from the beginFile fn : ",type(inputFile),"   ",inputFile.GetName())
			filenameForJson = (inputFile.GetName().strip().split('/')[-1]).split('.')[-2]
			self.filename = filenameForJson
			self.XS = self.xsInfo[self.filename]['XS'] * 1e-12
			self.totalNumberOfEvents = self.countsInfo[self.filename]
			print(" Filename for JSON : ",self.filename," XS = ",self.XS," sumofgenwts = ",self.totalNumberOfEvents)
			#1. Add the XS and Lumi Scaling for the event
			self.out.branch("xsWeight","F")

			#2. Add the Top gen level pt reweighting for TTbar Samples
			self.out.branch("topptWeight","F")
			self.out.branch("Top_wt","F")
			self.out.branch("genTop_pt","F")
			self.out.branch("antiTop_wt","F")
			self.out.branch("genantiTop_pt","F")

			#3. W and Z gen pt weights
			self.out.branch("ewkWWeight", "F")
			self.out.branch("ewkZWeight", "F")
			self.out.branch("ewkWDeborahsWeight", "F")
			self.out.branch("ewkZDeborahsWeight", "F")
			self.out.branch("qcdWWeight", "F")
			self.out.branch("qcdZTo2LWeight", "F")
			self.out.branch("GenV_pt", "F")
			self.out.branch("WnnloWeight","F")
			self.out.branch("ZnnloWeight","F")
			self.out.branch("combinedWZgenPtWeight","F")
			self.out.branch("combinedWZgenPtDeborahWeight","F")
			self.out.branch("combinedWZgenPtDylanWeight","F")

			##Systematics - QCD Scale Factors (for W and Z weights)
			self.out.branch("qcdWWeightRenUp", "F")
			self.out.branch("qcdWWeightRenDown", "F")
			self.out.branch("qcdWWeightFacUp", "F")
			self.out.branch("qcdWWeightFacDown", "F")
			self.out.branch("qcdZTo2LWeightRenUp", "F")
			self.out.branch("qcdZTo2LWeightRenDown", "F")
			self.out.branch("qcdZTo2LWeightFacUp", "F")
			self.out.branch("qcdZTo2LWeightFacDown", "F")

			#4. pile up weights
			self.out.branch("pileupcorrWeight","F")
			self.out.branch("pileupcorrWeightUp","F")
			self.out.branch("pileupcorrWeightDown","F")

			#5. btagging AK4 weights
			self.out.branch("btagmediumWeight","F")
			self.out.branch("btagmediumWeightbcUp","F")
			self.out.branch("btagmediumWeightbcDown","F")
			self.out.branch("btagmediumWeightbc%sUp"%(self.year),"F")
			self.out.branch("btagmediumWeightbc%sDown"%(self.year),"F")
			self.out.branch("btagmediumWeightlightUp","F")		
			self.out.branch("btagmediumWeightlightDown","F")
			self.out.branch("btagmediumWeightlight%sUp"%(self.year),"F")
			self.out.branch("btagmediumWeightlight%sDown"%(self.year),"F")

			self.out.branch("btagtightWeight","F")
			self.out.branch("btagtightWeightbcUp","F")
			self.out.branch("btagtightWeightbcDown","F")
			self.out.branch("btagtightWeightbc%sUp"%(self.year),"F")
			self.out.branch("btagtightWeightbc%sDown"%(self.year),"F")
			self.out.branch("btagtightWeightlightUp","F")		
			self.out.branch("btagtightWeightlightDown","F")
			self.out.branch("btagtightWeightlight%sUp"%(self.year),"F")
			self.out.branch("btagtightWeightlight%sDown"%(self.year),"F")
			#--->>Here we need separate nominal branches for the jet and the met variations
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("btagmediumWeight%s"%(sys),"F")
					self.out.branch("btagtightWeight%s"%(sys),"F")

			#6. ElectronId and Reco weights
			self.out.branch("eleidWeight","F")
			self.out.branch("eleidWeightUp","F")
			self.out.branch("eleidWeightDown","F")
			self.out.branch("elerecoWeight","F")
			self.out.branch("elerecoWeightUp","F")
			self.out.branch("elerecoWeightDown","F")
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("eleidWeight%s"%(sys),"F")
					self.out.branch("elerecoWeight%s"%(sys),"F")

			#6. MuonId and Iso weights
			self.out.branch("muonidWeight","F")
			self.out.branch("muonidWeightUp","F")
			self.out.branch("muonidWeightDown","F")
			self.out.branch("muonisoWeight","F")
			self.out.branch("muonisoWeightUp","F")
			self.out.branch("muonisoWeightDown","F")
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("muonidWeight%s"%(sys),"F")
					self.out.branch("muonisoWeight%s"%(sys),"F")

			#7. HPS DeepTauID v2p5 SFs
			self.out.branch("hpstauidWeight","F")
			self.out.branch("hpstauidWeightUp","F")
			self.out.branch("hpstauidWeightDown","F")
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("hpstauidWeight%s"%(sys),"F")

			#7. MET trigger SFs
			self.out.branch("metsfWeight","F")
			self.out.branch("metsfWeightUp","F")
			self.out.branch("metsfWeightDown","F")
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("metsfWeight%s"%(sys),"F")

			#8. AK8 particle net weight and systematics
			self.out.branch("Fatjet_pnet_bbvsqcd","F")
			self.out.branch("hbbloose","I")
			self.out.branch("hbblooseWeight","F")
			self.out.branch("hbblooseWeightUp","F")
			self.out.branch("hbblooseWeightDown","F")
			if not self.runNominal:
				for sys in self.jesUnc:
					self.out.branch("softdropmass%s"%(sys),"F")
					self.out.branch("softdropmassnom%s"%(sys),"F")
					self.out.branch("pnetmass%s"%(sys),"F")
					self.out.branch("hbblooseWeight%s"%(sys),"F")
					self.out.branch("hbbloose%s"%(sys),"I")
					self.out.branch("Fatjet_pnet_bbvsqcd%s"%(sys),"F")
		elif (self.isData):
			self.out.branch("Fatjet_pnet_bbvsqcd","F")
			self.out.branch("hbbloose","I")



	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass

	def analyze(self, event):
		def getAK4coll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_JetsUnclustUp, event.index_gJetsUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_JetsUnclustDown, event.index_gJetsUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_JetsjesTotalUp, event.index_gJetsjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_JetsjesTotalDown, event.index_gJetsjesTotalDown
			elif sys == "jerUp":
				return event.ngood_JetsjerUp, event.index_gJetsjerUp
			elif sys == "jerDown":
				return event.ngood_JetsjerDown, event.index_gJetsjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_JetsjesAbsoluteUp, event.index_gJetsjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_JetsjesAbsoluteDown, event.index_gJetsjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesAbsolute_2016Up, event.index_gJetsjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesAbsolute_2017Up, event.index_gJetsjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesAbsolute_2018Up, event.index_gJetsjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesAbsolute_2016Down, event.index_gJetsjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesAbsolute_2017Down, event.index_gJetsjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesAbsolute_2018Down, event.index_gJetsjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_JetsjesBBEC1Up, event.index_gJetsjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_JetsjesBBEC1Down, event.index_gJetsjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesBBEC1_2016Up, event.index_gJetsjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesBBEC1_2017Up, event.index_gJetsjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesBBEC1_2018Up, event.index_gJetsjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesBBEC1_2016Down, event.index_gJetsjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesBBEC1_2017Down, event.index_gJetsjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesBBEC1_2018Down, event.index_gJetsjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_JetsjesEC2Up, event.index_gJetsjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_JetsjesEC2Down, event.index_gJetsjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesEC2_2016Up, event.index_gJetsjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesEC2_2017Up, event.index_gJetsjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesEC2_2018Up, event.index_gJetsjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesEC2_2016Down, event.index_gJetsjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesEC2_2017Down, event.index_gJetsjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesEC2_2018Down, event.index_gJetsjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_JetsjesFlavorQCDUp, event.index_gJetsjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_JetsjesFlavorQCDDown, event.index_gJetsjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_JetsjesHFUp, event.index_gJetsjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_JetsjesHFDown, event.index_gJetsjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesHF_2016Up, event.index_gJetsjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesHF_2017Up, event.index_gJetsjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesHF_2018Up, event.index_gJetsjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesHF_2016Down, event.index_gJetsjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesHF_2017Down, event.index_gJetsjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesHF_2018Down, event.index_gJetsjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_JetsjesRelativeBalUp, event.index_gJetsjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_JetsjesRelativeBalDown, event.index_gJetsjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesRelativeSample_2016Up, event.index_gJetsjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesRelativeSample_2017Up, event.index_gJetsjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesRelativeSample_2018Up, event.index_gJetsjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_JetsjesRelativeSample_2016Down, event.index_gJetsjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_JetsjesRelativeSample_2017Down, event.index_gJetsjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_JetsjesRelativeSample_2018Down, event.index_gJetsjesRelativeSample_2018Down

		def getAK8coll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_FatJetsUnclustUp, event.index_gFatJetsUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_FatJetsUnclustDown, event.index_gFatJetsUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_FatJetsjesTotalUp, event.index_gFatJetsjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_FatJetsjesTotalDown, event.index_gFatJetsjesTotalDown
			elif sys == "jerUp":
				return event.ngood_FatJetsjerUp, event.index_gFatJetsjerUp
			elif sys == "jerDown":
				return event.ngood_FatJetsjerDown, event.index_gFatJetsjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_FatJetsjesAbsoluteUp, event.index_gFatJetsjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_FatJetsjesAbsoluteDown, event.index_gFatJetsjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesAbsolute_2016Up, event.index_gFatJetsjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesAbsolute_2017Up, event.index_gFatJetsjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesAbsolute_2018Up, event.index_gFatJetsjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesAbsolute_2016Down, event.index_gFatJetsjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesAbsolute_2017Down, event.index_gFatJetsjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesAbsolute_2018Down, event.index_gFatJetsjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_FatJetsjesBBEC1Up, event.index_gFatJetsjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_FatJetsjesBBEC1Down, event.index_gFatJetsjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesBBEC1_2016Up, event.index_gFatJetsjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesBBEC1_2017Up, event.index_gFatJetsjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesBBEC1_2018Up, event.index_gFatJetsjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesBBEC1_2016Down, event.index_gFatJetsjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesBBEC1_2017Down, event.index_gFatJetsjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesBBEC1_2018Down, event.index_gFatJetsjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_FatJetsjesEC2Up, event.index_gFatJetsjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_FatJetsjesEC2Down, event.index_gFatJetsjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesEC2_2016Up, event.index_gFatJetsjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesEC2_2017Up, event.index_gFatJetsjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesEC2_2018Up, event.index_gFatJetsjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesEC2_2016Down, event.index_gFatJetsjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesEC2_2017Down, event.index_gFatJetsjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesEC2_2018Down, event.index_gFatJetsjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_FatJetsjesFlavorQCDUp, event.index_gFatJetsjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_FatJetsjesFlavorQCDDown, event.index_gFatJetsjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_FatJetsjesHFUp, event.index_gFatJetsjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_FatJetsjesHFDown, event.index_gFatJetsjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesHF_2016Up, event.index_gFatJetsjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesHF_2017Up, event.index_gFatJetsjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesHF_2018Up, event.index_gFatJetsjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesHF_2016Down, event.index_gFatJetsjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesHF_2017Down, event.index_gFatJetsjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesHF_2018Down, event.index_gFatJetsjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_FatJetsjesRelativeBalUp, event.index_gFatJetsjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_FatJetsjesRelativeBalDown, event.index_gFatJetsjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesRelativeSample_2016Up, event.index_gFatJetsjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesRelativeSample_2017Up, event.index_gFatJetsjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesRelativeSample_2018Up, event.index_gFatJetsjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_FatJetsjesRelativeSample_2016Down, event.index_gFatJetsjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_FatJetsjesRelativeSample_2017Down, event.index_gFatJetsjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_FatJetsjesRelativeSample_2018Down, event.index_gFatJetsjesRelativeSample_2018Down

		def getElectroncoll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_ElectronsUnclustUp, event.index_gElectronsUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_ElectronsUnclustDown, event.index_gElectronsUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_ElectronsjesTotalUp, event.index_gElectronsjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_ElectronsjesTotalDown, event.index_gElectronsjesTotalDown
			elif sys == "jerUp":
				return event.ngood_ElectronsjerUp, event.index_gElectronsjerUp
			elif sys == "jerDown":
				return event.ngood_ElectronsjerDown, event.index_gElectronsjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_ElectronsjesAbsoluteUp, event.index_gElectronsjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_ElectronsjesAbsoluteDown, event.index_gElectronsjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesAbsolute_2016Up, event.index_gElectronsjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesAbsolute_2017Up, event.index_gElectronsjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesAbsolute_2018Up, event.index_gElectronsjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesAbsolute_2016Down, event.index_gElectronsjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesAbsolute_2017Down, event.index_gElectronsjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesAbsolute_2018Down, event.index_gElectronsjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_ElectronsjesBBEC1Up, event.index_gElectronsjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_ElectronsjesBBEC1Down, event.index_gElectronsjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesBBEC1_2016Up, event.index_gElectronsjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesBBEC1_2017Up, event.index_gElectronsjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesBBEC1_2018Up, event.index_gElectronsjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesBBEC1_2016Down, event.index_gElectronsjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesBBEC1_2017Down, event.index_gElectronsjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesBBEC1_2018Down, event.index_gElectronsjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_ElectronsjesEC2Up, event.index_gElectronsjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_ElectronsjesEC2Down, event.index_gElectronsjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesEC2_2016Up, event.index_gElectronsjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesEC2_2017Up, event.index_gElectronsjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesEC2_2018Up, event.index_gElectronsjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesEC2_2016Down, event.index_gElectronsjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesEC2_2017Down, event.index_gElectronsjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesEC2_2018Down, event.index_gElectronsjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_ElectronsjesFlavorQCDUp, event.index_gElectronsjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_ElectronsjesFlavorQCDDown, event.index_gElectronsjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_ElectronsjesHFUp, event.index_gElectronsjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_ElectronsjesHFDown, event.index_gElectronsjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesHF_2016Up, event.index_gElectronsjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesHF_2017Up, event.index_gElectronsjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesHF_2018Up, event.index_gElectronsjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesHF_2016Down, event.index_gElectronsjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesHF_2017Down, event.index_gElectronsjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesHF_2018Down, event.index_gElectronsjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_ElectronsjesRelativeBalUp, event.index_gElectronsjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_ElectronsjesRelativeBalDown, event.index_gElectronsjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesRelativeSample_2016Up, event.index_gElectronsjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesRelativeSample_2017Up, event.index_gElectronsjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesRelativeSample_2018Up, event.index_gElectronsjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_ElectronsjesRelativeSample_2016Down, event.index_gElectronsjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_ElectronsjesRelativeSample_2017Down, event.index_gElectronsjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_ElectronsjesRelativeSample_2018Down, event.index_gElectronsjesRelativeSample_2018Down

		def getMuoncoll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_MuonsUnclustUp, event.index_gMuonsUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_MuonsUnclustDown, event.index_gMuonsUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_MuonsjesTotalUp, event.index_gMuonsjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_MuonsjesTotalDown, event.index_gMuonsjesTotalDown
			elif sys == "jerUp":
				return event.ngood_MuonsjerUp, event.index_gMuonsjerUp
			elif sys == "jerDown":
				return event.ngood_MuonsjerDown, event.index_gMuonsjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_MuonsjesAbsoluteUp, event.index_gMuonsjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_MuonsjesAbsoluteDown, event.index_gMuonsjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesAbsolute_2016Up, event.index_gMuonsjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesAbsolute_2017Up, event.index_gMuonsjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesAbsolute_2018Up, event.index_gMuonsjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesAbsolute_2016Down, event.index_gMuonsjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesAbsolute_2017Down, event.index_gMuonsjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesAbsolute_2018Down, event.index_gMuonsjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_MuonsjesBBEC1Up, event.index_gMuonsjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_MuonsjesBBEC1Down, event.index_gMuonsjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesBBEC1_2016Up, event.index_gMuonsjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesBBEC1_2017Up, event.index_gMuonsjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesBBEC1_2018Up, event.index_gMuonsjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesBBEC1_2016Down, event.index_gMuonsjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesBBEC1_2017Down, event.index_gMuonsjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesBBEC1_2018Down, event.index_gMuonsjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_MuonsjesEC2Up, event.index_gMuonsjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_MuonsjesEC2Down, event.index_gMuonsjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesEC2_2016Up, event.index_gMuonsjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesEC2_2017Up, event.index_gMuonsjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesEC2_2018Up, event.index_gMuonsjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesEC2_2016Down, event.index_gMuonsjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesEC2_2017Down, event.index_gMuonsjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesEC2_2018Down, event.index_gMuonsjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_MuonsjesFlavorQCDUp, event.index_gMuonsjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_MuonsjesFlavorQCDDown, event.index_gMuonsjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_MuonsjesHFUp, event.index_gMuonsjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_MuonsjesHFDown, event.index_gMuonsjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesHF_2016Up, event.index_gMuonsjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesHF_2017Up, event.index_gMuonsjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesHF_2018Up, event.index_gMuonsjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesHF_2016Down, event.index_gMuonsjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesHF_2017Down, event.index_gMuonsjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesHF_2018Down, event.index_gMuonsjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_MuonsjesRelativeBalUp, event.index_gMuonsjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_MuonsjesRelativeBalDown, event.index_gMuonsjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesRelativeSample_2016Up, event.index_gMuonsjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesRelativeSample_2017Up, event.index_gMuonsjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesRelativeSample_2018Up, event.index_gMuonsjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_MuonsjesRelativeSample_2016Down, event.index_gMuonsjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_MuonsjesRelativeSample_2017Down, event.index_gMuonsjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_MuonsjesRelativeSample_2018Down, event.index_gMuonsjesRelativeSample_2018Down

		def getHPStaucoll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_TausUnclustUp, event.index_gTausUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_TausUnclustDown, event.index_gTausUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_TausjesTotalUp, event.index_gTausjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_TausjesTotalDown, event.index_gTausjesTotalDown
			elif sys == "jerUp":
				return event.ngood_TausjerUp, event.index_gTausjerUp
			elif sys == "jerDown":
				return event.ngood_TausjerDown, event.index_gTausjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_TausjesAbsoluteUp, event.index_gTausjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_TausjesAbsoluteDown, event.index_gTausjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesAbsolute_2016Up, event.index_gTausjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesAbsolute_2017Up, event.index_gTausjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesAbsolute_2018Up, event.index_gTausjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesAbsolute_2016Down, event.index_gTausjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesAbsolute_2017Down, event.index_gTausjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesAbsolute_2018Down, event.index_gTausjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_TausjesBBEC1Up, event.index_gTausjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_TausjesBBEC1Down, event.index_gTausjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesBBEC1_2016Up, event.index_gTausjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesBBEC1_2017Up, event.index_gTausjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesBBEC1_2018Up, event.index_gTausjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesBBEC1_2016Down, event.index_gTausjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesBBEC1_2017Down, event.index_gTausjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesBBEC1_2018Down, event.index_gTausjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_TausjesEC2Up, event.index_gTausjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_TausjesEC2Down, event.index_gTausjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesEC2_2016Up, event.index_gTausjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesEC2_2017Up, event.index_gTausjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesEC2_2018Up, event.index_gTausjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesEC2_2016Down, event.index_gTausjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesEC2_2017Down, event.index_gTausjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesEC2_2018Down, event.index_gTausjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_TausjesFlavorQCDUp, event.index_gTausjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_TausjesFlavorQCDDown, event.index_gTausjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_TausjesHFUp, event.index_gTausjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_TausjesHFDown, event.index_gTausjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesHF_2016Up, event.index_gTausjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesHF_2017Up, event.index_gTausjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesHF_2018Up, event.index_gTausjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesHF_2016Down, event.index_gTausjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesHF_2017Down, event.index_gTausjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesHF_2018Down, event.index_gTausjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_TausjesRelativeBalUp, event.index_gTausjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_TausjesRelativeBalDown, event.index_gTausjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesRelativeSample_2016Up, event.index_gTausjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesRelativeSample_2017Up, event.index_gTausjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesRelativeSample_2018Up, event.index_gTausjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_TausjesRelativeSample_2016Down, event.index_gTausjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_TausjesRelativeSample_2017Down, event.index_gTausjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_TausjesRelativeSample_2018Down, event.index_gTausjesRelativeSample_2018Down

		def getBoostedtaucoll(sys):
			if (sys == "UnclustUp"):
				return event.ngood_boostedTausUnclustUp, event.index_gboostedTausUnclustUp
			elif (sys == "UnclustDown"):
				return event.ngood_boostedTausUnclustDown, event.index_gboostedTausUnclustDown
			elif sys == "jesTotalUp":
				return event.ngood_boostedTausjesTotalUp, event.index_gboostedTausjesTotalUp
			elif sys == "jesTotalDown":
				return event.ngood_boostedTausjesTotalDown, event.index_gboostedTausjesTotalDown
			elif sys == "jerUp":
				return event.ngood_boostedTausjerUp, event.index_gboostedTausjerUp
			elif sys == "jerDown":
				return event.ngood_boostedTausjerDown, event.index_gboostedTausjerDown
			elif sys == "jesAbsoluteUp":
				return event.ngood_boostedTausjesAbsoluteUp, event.index_gboostedTausjesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.ngood_boostedTausjesAbsoluteDown, event.index_gboostedTausjesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesAbsolute_2016Up, event.index_gboostedTausjesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesAbsolute_2017Up, event.index_gboostedTausjesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesAbsolute_2018Up, event.index_gboostedTausjesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesAbsolute_2016Down, event.index_gboostedTausjesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesAbsolute_2017Down, event.index_gboostedTausjesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesAbsolute_2018Down, event.index_gboostedTausjesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.ngood_boostedTausjesBBEC1Up, event.index_gboostedTausjesBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.ngood_boostedTausjesBBEC1Down, event.index_gboostedTausjesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesBBEC1_2016Up, event.index_gboostedTausjesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesBBEC1_2017Up, event.index_gboostedTausjesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesBBEC1_2018Up, event.index_gboostedTausjesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesBBEC1_2016Down, event.index_gboostedTausjesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesBBEC1_2017Down, event.index_gboostedTausjesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesBBEC1_2018Down, event.index_gboostedTausjesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.ngood_boostedTausjesEC2Up, event.index_gboostedTausjesEC2Up
			elif sys == "jesEC2Down":
				return event.ngood_boostedTausjesEC2Down, event.index_gboostedTausjesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesEC2_2016Up, event.index_gboostedTausjesEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesEC2_2017Up, event.index_gboostedTausjesEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesEC2_2018Up, event.index_gboostedTausjesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesEC2_2016Down, event.index_gboostedTausjesEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesEC2_2017Down, event.index_gboostedTausjesEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesEC2_2018Down, event.index_gboostedTausjesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.ngood_boostedTausjesFlavorQCDUp, event.index_gboostedTausjesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.ngood_boostedTausjesFlavorQCDDown, event.index_gboostedTausjesFlavorQCDDown
			elif sys == "jesHFUp":
				return event.ngood_boostedTausjesHFUp, event.index_gboostedTausjesHFUp
			elif sys == "jesHFDown":
				return event.ngood_boostedTausjesHFDown, event.index_gboostedTausjesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesHF_2016Up, event.index_gboostedTausjesHF_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesHF_2017Up, event.index_gboostedTausjesHF_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesHF_2018Up, event.index_gboostedTausjesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesHF_2016Down, event.index_gboostedTausjesHF_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesHF_2017Down, event.index_gboostedTausjesHF_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesHF_2018Down, event.index_gboostedTausjesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.ngood_boostedTausjesRelativeBalUp, event.index_gboostedTausjesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.ngood_boostedTausjesRelativeBalDown, event.index_gboostedTausjesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesRelativeSample_2016Up, event.index_gboostedTausjesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesRelativeSample_2017Up, event.index_gboostedTausjesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesRelativeSample_2018Up, event.index_gboostedTausjesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.ngood_boostedTausjesRelativeSample_2016Down, event.index_gboostedTausjesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.ngood_boostedTausjesRelativeSample_2017Down, event.index_gboostedTausjesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.ngood_boostedTausjesRelativeSample_2018Down, event.index_gboostedTausjesRelativeSample_2018Down

		def getMETpt(sys):
			if sys == "":
				return event.METcorrected_pt
			elif sys == "jesTotalUp":
				return event.METcorrected_ptScaleUp
			elif sys == "jesTotalDown":
				return event.METcorrected_ptScaleDown
			elif sys == "jerUp":
				return event.METcorrected_ptResUp
			elif sys == "jerDown":
				return event.METcorrected_ptResDown
			elif sys == "jesAbsoluteUp":
				return event.METcorrected_ptScaleAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return event.METcorrected_ptScaleAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return event.METcorrected_ptScaleBBEC1Up
			elif sys == "jesBBEC1Down":
				return event.METcorrected_ptScaleBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleBBEC1_2018Down
			elif sys == "jesEC2Up":
				return event.METcorrected_ptScaleEC2Up
			elif sys == "jesEC2Down":
				return event.METcorrected_ptScaleEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleEC2_2016Up
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleEC2_2017Up
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleEC2_2016Down
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleEC2_2017Down
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return event.METcorrected_ptScaleFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return event.METcorrected_ptScaleFlavorQCDDown
			elif sys == "jesHFUp":
				return event.METcorrected_ptScaleHFUp
			elif sys == "jesHFDown":
				return event.METcorrected_ptScaleHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleHF_2016Up
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleHF_2017Up
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleHF_2016Down
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleHF_2017Down
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleHF_2018Down
			elif sys == "jesRelativeBalUp":
				return event.METcorrected_ptScaleRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return event.METcorrected_ptScaleRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return event.METcorrected_ptScaleRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return event.METcorrected_ptScaleRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return event.METcorrected_ptScaleRelativeSample_2018Down
			elif sys == "UnclustUp":
				return event.METcorrected_ptUnclustUp
			elif sys == "UnclustDown":
				return event.METcorrected_ptUnclustDown

		def getjetpt(jet, sys):
			if ((sys == "") or (sys == "UnclustUp") or (sys == "UnclustDown")):
				return jet.pt_nom
			elif sys == "jesTotalUp":
				return jet.pt_jesTotalUp
			elif sys == "jesTotalDown":
				return jet.pt_jesTotalDown
			elif sys == "jerUp":
				return jet.pt_jerUp
			elif sys == "jerDown":
				return jet.pt_jerDown
			elif sys == "jesAbsoluteUp":
				return jet.pt_jesAbsoluteUp
			elif sys == "jesAbsoluteDown":
				return jet.pt_jesAbsoluteDown
			elif sys == "jesAbsolute_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesAbsolute_2016Up
				elif (self.year_unc=="2017"):
					return jet.pt_jesAbsolute_2017Up
				elif (self.year_unc=="2018"):
					return jet.pt_jesAbsolute_2018Up
			elif sys == "jesAbsolute_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesAbsolute_2016Down
				elif (self.year_unc=="2017"):
					return jet.pt_jesAbsolute_2017Down
				elif (self.year_unc=="2018"):
					return jet.pt_jesAbsolute_2018Down
			elif sys == "jesBBEC1Up":
				return jet.pt_jesBBEC1Up
			elif sys == "jesBBEC1Down":
				return jet.pt_jesBBEC1Down
			elif sys == "jesBBEC1_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesBBEC1_2016Up
				elif (self.year_unc=="2017"):
					return jet.pt_jesBBEC1_2017Up
				elif (self.year_unc=="2018"):
					return jet.pt_jesBBEC1_2018Up
			elif sys =="jesBBEC1_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesBBEC1_2016Down
				elif (self.year_unc=="2017"):
					return jet.pt_jesBBEC1_2017Down
				elif (self.year_unc=="2018"):
					return jet.pt_jesBBEC1_2018Down
			elif sys == "jesEC2Up":
				return jet.pt_jesEC2Up
			elif sys == "jesEC2Down":
				return jet.pt_jesEC2Down
			elif sys == "jesEC2_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesEC2_2016Up
				elif (self.year_unc=="2017"):
					return jet.pt_jesEC2_2017Up
				elif (self.year_unc=="2018"):
					return jet.pt_jesEC2_2018Up
			elif sys =="jesEC2_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesEC2_2016Down
				elif (self.year_unc=="2017"):
					return jet.pt_jesEC2_2017Down
				elif (self.year_unc=="2018"):
					return jet.pt_jesEC2_2018Down
			elif sys == "jesFlavorQCDUp":
				return jet.pt_jesFlavorQCDUp
			elif sys == "jesFlavorQCDDown":
				return jet.pt_jesFlavorQCDDown
			elif sys == "jesHFUp":
				return jet.pt_jesHFUp
			elif sys == "jesHFDown":
				return jet.pt_jesHFDown
			elif sys == "jesHF_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesHF_2016Up
				elif (self.year_unc=="2017"):
					return jet.pt_jesHF_2017Up
				elif (self.year_unc=="2018"):
					return jet.pt_jesHF_2018Up
			elif sys =="jesHF_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesHF_2016Down
				elif (self.year_unc=="2017"):
					return jet.pt_jesHF_2017Down
				elif (self.year_unc=="2018"):
					return jet.pt_jesHF_2018Down
			elif sys == "jesRelativeBalUp":
				return jet.pt_jesRelativeBalUp
			elif sys == "jesRelativeBalDown":
				return jet.pt_jesRelativeBalDown
			elif sys == "jesRelativeSample_%sUp"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesRelativeSample_2016Up
				elif (self.year_unc=="2017"):
					return jet.pt_jesRelativeSample_2017Up
				elif (self.year_unc=="2018"):
					return jet.pt_jesRelativeSample_2018Up
			elif sys =="jesRelativeSample_%sDown"%(self.year_unc):
				if (self.year_unc=="2016"):
					return jet.pt_jesRelativeSample_2016Down
				elif (self.year_unc=="2017"):
					return jet.pt_jesRelativeSample_2017Down
				elif (self.year_unc=="2018"):
					return jet.pt_jesRelativeSample_2018Down

		ElectronCollection = Collection(event,'Electron','nElectron')
		MuonCollection = Collection(event,'Muon','nMuon')
		TauCollection = Collection(event,'Tau','nTau')

		if (self.isData):
			if (event.ngood_Muons==1):
				if (abs(MuonCollection[event.index_gMuons[0]].eta)>=2.4):
					print("Event rejected since Muon eta >= 2.4")
					return False
			
			fatjets = Collection(event, "FatJet")	

			if (event.ngood_FatJets>0):
				Fatjet_pnet_bbvsqcd = (fatjets[event.index_gFatJets[0]].particleNetLegacy_Xbb)/(fatjets[event.index_gFatJets[0]].particleNetLegacy_Xbb + fatjets[event.index_gFatJets[0]].particleNetLegacy_QCD)
				self.out.fillBranch("Fatjet_pnet_bbvsqcd",Fatjet_pnet_bbvsqcd)
				if(Fatjet_pnet_bbvsqcd>self.pnetloose):
					self.out.fillBranch("hbbloose",1)
				else:
					self.out.fillBranch("hbbloose",0)
			else:
				print("Number of Fatjets in..Nominal...is ZERO")
				self.out.fillBranch("Fatjet_pnet_bbvsqcd",-1.00)
				self.out.fillBranch("hbbloose",0)
			return True								


		#1. Add the XS and Lumi Scaling for the event
		xsWeight = (self.XS * self.LHCLumi * event.genWeight) / self.totalNumberOfEvents
		self.out.fillBranch("xsWeight",xsWeight)
		#Add up down variations if any?

		#2. Add the Top gen level pt reweighting for TTbar Samples
		SF_top = 1.0
		SF_antitop = 1.0
		#Compute the top reweighting
		if search("TTTo",self.filename):
			#print ("This is a TTbar sample : ",self.filename)
			genParticles = Collection(event, "GenPart")
			#Filter the genPart collection to pick out top (pdgid is 6) and make sure top quark in MC is defined at parton level, after radiation and before decay, using the 'isLastCopy' i.e status 62
			top = list(filter(lambda gen : (gen.pdgId == 6) and (gen.status == 62), genParticles))
			if len(top) > 0:
				SF_top = 0.103*np.exp(-0.0118*top[0].pt) - 0.000134*top[0].pt + 0.973
			
			#Repeat the same for antitop
			antitop = list(filter(lambda gen : (gen.pdgId == -6) and (gen.status == 62), genParticles))
			if len(antitop) > 0:
				SF_antitop = 0.103*np.exp(-0.0118*antitop[0].pt) - 0.000134*antitop[0].pt + 0.973
		
			#This branch is used for plotting "Top_pt_rwt"
			self.out.fillBranch("topptWeight",np.sqrt(SF_top*SF_antitop))
			self.out.fillBranch("Top_wt",SF_top)
			self.out.fillBranch("antiTop_wt",SF_antitop)
			self.out.fillBranch("genTop_pt",top[0].pt)
			self.out.fillBranch("genantiTop_pt",antitop[0].pt)
			#Add Up and Down Variations if any?

		else:
			self.out.fillBranch("topptWeight",1.0)
			self.out.fillBranch("Top_wt",1.0)
			self.out.fillBranch("antiTop_wt",1.0)
			self.out.fillBranch("genTop_pt",-99.99)
			self.out.fillBranch("genantiTop_pt",-99.99)
			#Add Up and Down Variations if any?

		#3. W and Z gen pt weights
		ewkWWeight = ewkZWeight = qcdWWeight = qcdZTo2LWeight = ewkWDeborahsWeight = ewkZDeborahsWeight = combinedWZgenPtDylanWeight = WnnloWeight = ZnnloWeight = combinedWZgenPtWeight = combinedWZgenPtDeborahWeight = 1
		qcdWWeightRenUp = qcdWWeightRenDown = qcdWWeightFacUp = qcdWWeightFacDown = 1
		qcdZTo2LWeightRenUp = qcdZTo2LWeightRenDown = qcdZTo2LWeightFacUp = qcdZTo2LWeightFacDown = 1
		GenV_pt = -9
		GenV = []
		if (search("DYJetsToLL_M-50",self.filename)):
			genParticles = Collection(event, "GenPart")
			GenV = list(filter(lambda gen : (gen.pdgId == 23) and (gen.status == 22), genParticles))
			if len(GenV) > 0:
				GenV_pt = GenV[0].pt
				ewkZWeight *= self.kFactorTool.getEWKZ(GenV_pt)
				ewkZDeborahsWeight *= self.kFactorTool.getDeborahEWKZ(GenV_pt)
				qcdZTo2LWeight *= self.kFactorTool.getQCDZTo2L(GenV_pt)
				qcdZTo2LWeightRenUp *= self.kFactorTool.getRenUpZTo2L(GenV_pt)
				qcdZTo2LWeightRenDown *= self.kFactorTool.getRenDownZTo2L(GenV_pt)
				qcdZTo2LWeightFacUp *= self.kFactorTool.getFacUpZTo2L(GenV_pt)
				qcdZTo2LWeightFacDown *= self.kFactorTool.getFacDownZTo2L(GenV_pt)
				ZnnloWeight = 0.934 

				if (self.year=="2016APV"):
					combinedWZgenPtWeight = qcdZTo2LWeight*ewkZWeight
					combinedWZgenPtDeborahWeight = qcdZTo2LWeight*ewkZDeborahsWeight
				elif (self.year=="2016"):
					combinedWZgenPtWeight = qcdZTo2LWeight*ewkZWeight
					combinedWZgenPtDeborahWeight = qcdZTo2LWeight*ewkZDeborahsWeight				
				elif (self.year=="2017"):
					combinedWZgenPtWeight = qcdZTo2LWeight*ewkZWeight*0.934  
					combinedWZgenPtDeborahWeight = qcdZTo2LWeight*ewkZDeborahsWeight*0.934				
				elif (self.year=="2018"):
					combinedWZgenPtWeight = qcdZTo2LWeight*ewkZWeight*0.934  
					combinedWZgenPtDeborahWeight = qcdZTo2LWeight*ewkZDeborahsWeight*0.934

			combinedWZgenPtDylanWeight = 1.23
				#combinedWZgenPtWeight = qcdZTo2LWeight*ewkZWeight*0.934  
				#combinedWZgenPtDeborahWeight = qcdZTo2LWeight*ewkZDeborahsWeight*0.934           

		elif(search("WJet",self.filename)):
			genParticles = Collection(event, "GenPart")
			GenV = list(filter(lambda gen : (abs(gen.pdgId) == 24) and gen.status == 22, genParticles))   
			if len(GenV) > 0:
				GenV_pt = GenV[0].pt
				ewkWWeight *= self.kFactorTool.getEWKW(GenV_pt)
				ewkWDeborahsWeight *= self.kFactorTool.getDeborahEWKW(GenV_pt)
				qcdWWeight *= self.kFactorTool.getQCDW(GenV_pt)
				qcdWWeightRenUp *= self.kFactorTool.getRenUpW(GenV_pt)
				qcdWWeightRenDown *= self.kFactorTool.getRenDownW(GenV_pt)
				qcdWWeightFacUp *= self.kFactorTool.getFacUpW(GenV_pt)
				qcdWWeightFacDown *= self.kFactorTool.getFacDownW(GenV_pt)
				WnnloWeight = 0.9135
				if (self.year=="2016APV"):
					combinedWZgenPtWeight = qcdWWeight*ewkWWeight
					combinedWZgenPtDeborahWeight = qcdWWeight*ewkWDeborahsWeight #VERIFY again..Deborah said QCD to be taken from python for 2016 but we have all same tunes unlike victor				
				elif (self.year=="2016"):
					combinedWZgenPtWeight = qcdWWeight*ewkWWeight
					combinedWZgenPtDeborahWeight = qcdWWeight*ewkWDeborahsWeight #VERIFY again..Deborah said QCD to be taken from python for 2016 but we have all same tunes unlike victor			
				elif (self.year=="2017"):
					combinedWZgenPtWeight = qcdWWeight*ewkWWeight*0.9135
					combinedWZgenPtDeborahWeight = qcdWWeight*ewkWDeborahsWeight*0.9135				
				elif (self.year=="2018"):
					combinedWZgenPtWeight = qcdWWeight*ewkWWeight*0.9135
					combinedWZgenPtDeborahWeight = qcdWWeight*ewkWDeborahsWeight*0.9135
				
			combinedWZgenPtDylanWeight = 1.21
				#combinedWZgenPtWeight = qcdWWeight*ewkWWeight*0.9135
				#combinedWZgenPtDeborahWeight = qcdWWeight*ewkWDeborahsWeight*0.9135

		#--->Nominal Weights
		self.out.fillBranch("ewkWWeight", ewkWWeight)
		self.out.fillBranch("ewkZWeight", ewkZWeight)
		self.out.fillBranch("ewkWDeborahsWeight", ewkWDeborahsWeight)
		self.out.fillBranch("ewkZDeborahsWeight", ewkZDeborahsWeight)
		self.out.fillBranch("qcdWWeight", qcdWWeight)
		self.out.fillBranch("qcdZTo2LWeight", qcdZTo2LWeight)
		self.out.fillBranch("GenV_pt", GenV_pt)
		self.out.fillBranch("WnnloWeight",WnnloWeight)
		self.out.fillBranch("ZnnloWeight",ZnnloWeight)
		self.out.fillBranch("combinedWZgenPtWeight",combinedWZgenPtWeight)
		self.out.fillBranch("combinedWZgenPtDeborahWeight",combinedWZgenPtDeborahWeight)
		self.out.fillBranch("combinedWZgenPtDylanWeight",combinedWZgenPtDylanWeight)

		#--->systematics - QCD Scale Factors
		self.out.fillBranch("qcdWWeightRenUp", qcdWWeightRenUp)
		self.out.fillBranch("qcdWWeightRenDown", qcdWWeightRenDown)
		self.out.fillBranch("qcdWWeightFacUp", qcdWWeightFacUp)
		self.out.fillBranch("qcdWWeightFacDown", qcdWWeightFacDown)
		self.out.fillBranch("qcdZTo2LWeightRenUp", qcdZTo2LWeightRenUp)
		self.out.fillBranch("qcdZTo2LWeightRenDown", qcdZTo2LWeightRenDown)
		self.out.fillBranch("qcdZTo2LWeightFacUp", qcdZTo2LWeightFacUp)
		self.out.fillBranch("qcdZTo2LWeightFacDown", qcdZTo2LWeightFacDown)

		#4. pileup weights
		self.out.fillBranch("pileupcorrWeight",self.evaluator_pileup.evaluate(event.Pileup_nTrueInt,"nominal"))
		#--->systematics 
		self.out.fillBranch("pileupcorrWeightUp",self.evaluator_pileup.evaluate(event.Pileup_nTrueInt,"up"))
		self.out.fillBranch("pileupcorrWeightDown",self.evaluator_pileup.evaluate(event.Pileup_nTrueInt,"down"))

		#5. AK4 btagging weights
		jets = Collection(event, "Jet")
		#print("This is ngood_Jets variable = ", event.ngood_Jets,"....This is the index list....",event.index_gJets)
		jetsgood = [jets[index] for index in list(event.index_gJets)[:int(event.ngood_Jets)]]
		self.out.fillBranch("btagmediumWeight",self.btagTool.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightbcUp",self.btagToolbcUpCorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightbcDown",self.btagToolbcDownCorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightbc%sUp"%(self.year),self.btagToolbcUpUncorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightbc%sDown"%(self.year),self.btagToolbcDownUncorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightlightUp",self.btagToollightUpCorrelated.getWeight(jetsgood,""))		
		self.out.fillBranch("btagmediumWeightlightDown",self.btagToollightDownCorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightlight%sUp"%(self.year),self.btagToollightUpUncorrelated.getWeight(jetsgood,""))
		self.out.fillBranch("btagmediumWeightlight%sDown"%(self.year),self.btagToollightDownUncorrelated.getWeight(jetsgood,""))

		self.out.fillBranch("btagtightWeight",self.btagToolTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightbcUp",self.btagToolbcUpCorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightbcDown",self.btagToolbcDownCorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightbc%sUp"%(self.year),self.btagToolbcUpUncorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightbc%sDown"%(self.year),self.btagToolbcDownUncorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightlightUp",self.btagToollightUpCorrelatedTight.getWeight(jetsgood,""))		
		self.out.fillBranch("btagtightWeightlightDown",self.btagToollightDownCorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightlight%sUp"%(self.year),self.btagToollightUpUncorrelatedTight.getWeight(jetsgood,""))
		self.out.fillBranch("btagtightWeightlight%sDown"%(self.year),self.btagToollightDownUncorrelatedTight.getWeight(jetsgood,""))

		if not self.runNominal:
			for sys in self.jesUnc:
				#jetsgood = [jets[index] for index in event.index_gJets[:event.ngood_Jets]]
				jetsgood = [jets[index] for index in list(getAK4coll(sys)[1])[:int(getAK4coll(sys)[0])]]
				self.out.fillBranch("btagmediumWeight%s"%(sys),self.btagTool.getWeight(jetsgood,sys))
				self.out.fillBranch("btagtightWeight%s"%(sys),self.btagToolTight.getWeight(jetsgood,sys))
		
		#6. Electron Identification Weights
		if (event.ngood_Electrons==1):
			#ele_pt = float(event.Electron_pt[int(event.index_gElectrons[0])])
			#print("After ini = ",ele_pt,event.index_gElectrons)
			#ele_eta = float(event.Electron_eta[event.index_gElectrons[0]])
			#print ("channel = ",event.channel,"electron_pt = ",ele_pt,event.Electron_pt[event.index_gElectrons[0]],type(event.Electron_pt[event.index_gElectrons[0]]),"electron_eta = ",ele_eta,event.Electron_eta[event.index_gElectrons[0]])
			###print ("channel = ",event.channel,"electron_pt = ",ElectronCollection[event.index_gElectrons[0]].pt,"electron_eta = ",ElectronCollection[event.index_gElectrons[0]].eta)
			self.out.fillBranch("eleidWeight",self.evaluator_electronid.evaluate(self.year,"sf","Loose",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
			self.out.fillBranch("eleidWeightUp",self.evaluator_electronid.evaluate(self.year,"sfup","Loose",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
			self.out.fillBranch("eleidWeightDown",self.evaluator_electronid.evaluate(self.year,"sfdown","Loose",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
			if (ElectronCollection[event.index_gElectrons[0]].pt > 20):
				self.out.fillBranch("elerecoWeight",self.evaluator_electronid.evaluate(self.year,"sf","RecoAbove20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
				self.out.fillBranch("elerecoWeightUp",self.evaluator_electronid.evaluate(self.year,"sfup","RecoAbove20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
				self.out.fillBranch("elerecoWeightDown",self.evaluator_electronid.evaluate(self.year,"sfdown","RecoAbove20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
			else:
				self.out.fillBranch("elerecoWeight",self.evaluator_electronid.evaluate(self.year,"sf","RecoBelow20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
				self.out.fillBranch("elerecoWeightUp",self.evaluator_electronid.evaluate(self.year,"sfup","RecoBelow20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))
				self.out.fillBranch("elerecoWeightDown",self.evaluator_electronid.evaluate(self.year,"sfdown","RecoBelow20",ElectronCollection[event.index_gElectrons[0]].eta,ElectronCollection[event.index_gElectrons[0]].pt))

		else:
			self.out.fillBranch("eleidWeight",1.0)
			self.out.fillBranch("eleidWeightUp",1.0)
			self.out.fillBranch("eleidWeightDown",1.0)
			self.out.fillBranch("elerecoWeight",1.0)
			self.out.fillBranch("elerecoWeightUp",1.0)
			self.out.fillBranch("elerecoWeightDown",1.0)			

		if not self.runNominal:
			for sys in self.jesUnc:
				if (getElectroncoll(sys)[0] == 1):
					#ele_pt = event.Electron_pt[getElectroncoll(sys)[1][0]]
					#ele_eta = event.Electron_eta[getElectroncoll(sys)[1][0]]
					###print("For Electron channel sys =",sys,".....Ele pt = ",ElectronCollection[getElectroncoll(sys)[1][0]].pt,"...Ele eta = ",ElectronCollection[getElectroncoll(sys)[1][0]].eta)
					self.out.fillBranch("eleidWeight%s"%(sys),self.evaluator_electronid.evaluate(self.year,"sf","Loose",ElectronCollection[getElectroncoll(sys)[1][0]].eta,ElectronCollection[getElectroncoll(sys)[1][0]].pt))
					if (ElectronCollection[getElectroncoll(sys)[1][0]].pt > 20):
						self.out.fillBranch("elerecoWeight%s"%(sys),self.evaluator_electronid.evaluate(self.year,"sf","RecoAbove20",ElectronCollection[getElectroncoll(sys)[1][0]].eta,ElectronCollection[getElectroncoll(sys)[1][0]].pt))
					else:
						self.out.fillBranch("elerecoWeight%s"%(sys),self.evaluator_electronid.evaluate(self.year,"sf","RecoBelow20",ElectronCollection[getElectroncoll(sys)[1][0]].eta,ElectronCollection[getElectroncoll(sys)[1][0]].pt))					
				else:
					self.out.fillBranch("eleidWeight%s"%(sys),1.0)
					self.out.fillBranch("elerecoWeight%s"%(sys),1.0)								

		#6. Muon Identification Weights
		if (event.ngood_Muons==1):
			if (abs(MuonCollection[event.index_gMuons[0]].eta)>=2.4):
				print("Event rejected since Muon eta >= 2.4")
				return False
			#muo_pt = float(event.Muon_pt[int(event.index_gMuons[0])])
			#muo_eta = float(event.Muon_eta[event.index_gMuons[0]])
			#print ("channel = ",event.channel,"muon_pt = ",muo_pt,event.Muon_pt[event.index_gMuons[0]],type(event.index_gMuons[0]),"muon_eta = ",muo_eta,event.softdropmassnom)
			#print ("channel = ",event.channel,"muon_pt = ",MuonCollection[event.index_gMuons[0]].pt,"muon_eta = ",MuonCollection[event.index_gMuons[0]].eta)
			self.out.fillBranch("muonidWeight",self.evaluator_muonid.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"nominal"))
			self.out.fillBranch("muonidWeightUp",self.evaluator_muonid.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"systup"))
			self.out.fillBranch("muonidWeightDown",self.evaluator_muonid.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"systdown"))
			self.out.fillBranch("muonisoWeight",self.evaluator_muoniso.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"nominal"))
			self.out.fillBranch("muonisoWeightUp",self.evaluator_muoniso.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"systup"))
			self.out.fillBranch("muonisoWeightDown",self.evaluator_muoniso.evaluate(abs(MuonCollection[event.index_gMuons[0]].eta),MuonCollection[event.index_gMuons[0]].pt,"systdown"))
		else:
			self.out.fillBranch("muonidWeight",1.0)
			self.out.fillBranch("muonidWeightUp",1.0)
			self.out.fillBranch("muonidWeightDown",1.0)
			self.out.fillBranch("muonisoWeight",1.0)
			self.out.fillBranch("muonisoWeightUp",1.0)
			self.out.fillBranch("muonisoWeightDown",1.0)

		if not self.runNominal:
			for sys in self.jesUnc:
				if (getMuoncoll(sys)[0] == 1):
					if (abs(MuonCollection[getMuoncoll(sys)[1][0]].eta)>=2.4):
						print("Muon weight = 1 for sys due to Muon eta >= 2.4")
						self.out.fillBranch("muonidWeight%s"%(sys),1.0)
						self.out.fillBranch("muonisoWeight%s"%(sys),1.0)
						continue	
					#muo_pt = event.Muon_pt[getMuoncoll(sys)[1][0]]
					#muo_eta = event.Muon_eta[getMuoncoll(sys)[1][0]]
					#print("For Muon channel sys =",sys,".....Muo pt = ",MuonCollection[getMuoncoll(sys)[1][0]].pt,"...Ele eta = ",MuonCollection[getMuoncoll(sys)[1][0]].eta)
					self.out.fillBranch("muonidWeight%s"%(sys),self.evaluator_muonid.evaluate(abs(MuonCollection[getMuoncoll(sys)[1][0]].eta),MuonCollection[getMuoncoll(sys)[1][0]].pt,"nominal"))
					self.out.fillBranch("muonisoWeight%s"%(sys),self.evaluator_muonid.evaluate(abs(MuonCollection[getMuoncoll(sys)[1][0]].eta),MuonCollection[getMuoncoll(sys)[1][0]].pt,"nominal"))
				else:
					self.out.fillBranch("muonidWeight%s"%(sys),1.0)
					self.out.fillBranch("muonisoWeight%s"%(sys),1.0)

		#7. HPS tau ID Weights
		HPStauIDWeight = 1.0
		HPStauIDWeight_Up = 1.0
		HPStauIDWeight_Down = 1.0
		dmlist = [0,1,2,10,11]
		#print("Decay mode = ",[obj.decayMode for obj in TauCollection])
		for i in range(event.ngood_Taus):
			#print("number of good taus = ",event.ngood_Taus)
			if (TauCollection[event.index_gTaus[i]].genPartIdx>=0):
			#if (event.Tau_genPartIdx[event.index_gTaus[i]]>=0):
				if((TauCollection[event.index_gTaus[i]].pt<=140) and ((TauCollection[event.index_gTaus[i]].decayMode in dmlist))):
					HPStauIDWeight = HPStauIDWeight*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","nom","dm")									
					HPStauIDWeight_Up = HPStauIDWeight_Up*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","syst_alleras_up","dm")
					HPStauIDWeight_Down = HPStauIDWeight_Down*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","syst_alleras_down","dm")
				elif((TauCollection[event.index_gTaus[i]].pt>140)):
					#print("pt = ", TauCollection[event.index_gTaus[i]].pt," decay mode  = ", int(TauCollection[event.index_gTaus[i]].decayMode)," genpart = ",int(TauCollection[event.index_gTaus[i]].genPartFlav))
					HPStauIDWeight = HPStauIDWeight*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","nom","pt")					
					HPStauIDWeight_Up = HPStauIDWeight_Up*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","up","pt")
					HPStauIDWeight_Down = HPStauIDWeight_Down*self.evaluator_hpstauid.evaluate(TauCollection[event.index_gTaus[i]].pt,TauCollection[event.index_gTaus[i]].decayMode,TauCollection[event.index_gTaus[i]].genPartFlav,"Loose","VVLoose","down","pt")
		self.out.fillBranch("hpstauidWeight",HPStauIDWeight)
		self.out.fillBranch("hpstauidWeightUp",HPStauIDWeight_Up)
		self.out.fillBranch("hpstauidWeightDown",HPStauIDWeight_Down)
		
		if not self.runNominal:
			for sys in self.jesUnc:
				HPStauIDWeight = 1.0
				for i in range(getHPStaucoll(sys)[0]):
					if (TauCollection[getHPStaucoll(sys)[1][i]].genPartIdx>=0):
					#if (event.Tau_genPartIdx[getHPStaucoll(sys)[1][i]]>=0):
						if((TauCollection[getHPStaucoll(sys)[1][i]].pt<=140) and ((TauCollection[getHPStaucoll(sys)[1][i]].decayMode in dmlist))):
							HPStauIDWeight = HPStauIDWeight*self.evaluator_hpstauid.evaluate(TauCollection[getHPStaucoll(sys)[1][i]].pt,TauCollection[getHPStaucoll(sys)[1][i]].decayMode,TauCollection[getHPStaucoll(sys)[1][i]].genPartFlav,"Loose","VVLoose","nom","dm")									
						elif((TauCollection[getHPStaucoll(sys)[1][i]].pt >140)):
							HPStauIDWeight = HPStauIDWeight*self.evaluator_hpstauid.evaluate(TauCollection[getHPStaucoll(sys)[1][i]].pt,TauCollection[getHPStaucoll(sys)[1][i]].decayMode,TauCollection[getHPStaucoll(sys)[1][i]].genPartFlav,"Loose","VVLoose","nom","pt")					
				self.out.fillBranch("hpstauidWeight%s"%(sys),HPStauIDWeight)		
		
		#7. MET trigger SF weights
		triggerWeighting = 1.0
		triggerWeighting_Up = 1.0
		triggerWeighting_Down = 1.0

		if (event.METcorrected_pt>=180):
			if (event.METcorrected_pt >= 500):
				triggerWeighting = triggerWeighting*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetNbinsX())
				triggerWeighting_Up = triggerWeighting_Up*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetNbinsX()) + 0.50*(self.evaluator_sfHisto.GetBinError(self.evaluator_sfHisto.GetNbinsX()))
				triggerWeighting_Down = triggerWeighting_Down*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetNbinsX()) - 0.50*(self.evaluator_sfHisto.GetBinError(self.evaluator_sfHisto.GetNbinsX()))
			else:
				triggerWeighting = triggerWeighting*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetXaxis().FindBin(event.METcorrected_pt))
				triggerWeighting_Up = triggerWeighting_Up*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetXaxis().FindBin(event.METcorrected_pt)) + 0.50*(self.evaluator_sfHisto.GetBinError(self.evaluator_sfHisto.GetXaxis().FindBin(event.METcorrected_pt))) 			
				triggerWeighting_Down = triggerWeighting_Down*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetXaxis().FindBin(event.METcorrected_pt)) - 0.50*(self.evaluator_sfHisto.GetBinError(self.evaluator_sfHisto.GetXaxis().FindBin(event.METcorrected_pt)))

			self.out.fillBranch("metsfWeight",triggerWeighting)
			self.out.fillBranch("metsfWeightUp",triggerWeighting_Up)
			self.out.fillBranch("metsfWeightDown",triggerWeighting_Down)
		else:
			self.out.fillBranch("metsfWeight",-1.0)
			self.out.fillBranch("metsfWeightUp",-1.0)
			self.out.fillBranch("metsfWeightDown",-1.0)			

		if not self.runNominal:
			for sys in self.jesUnc:
				triggerWeighting = 1.0
				if(getMETpt(sys) >= 180):
					if (getMETpt(sys) >= 500):
						triggerWeighting = triggerWeighting*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetNbinsX())
					else:
						triggerWeighting = triggerWeighting*self.evaluator_sfHisto.GetBinContent(self.evaluator_sfHisto.GetXaxis().FindBin(getMETpt(sys)))	
					self.out.fillBranch("metsfWeight%s"%(sys),triggerWeighting)	
				else:
					self.out.fillBranch("metsfWeight%s"%(sys),-1.0)

		#8. Particle Net AK8 weights
		fatjets = Collection(event, "FatJet")	

		if (event.ngood_FatJets>0):
			Fatjet_pnet_bbvsqcd = (fatjets[event.index_gFatJets[0]].particleNetLegacy_Xbb)/(fatjets[event.index_gFatJets[0]].particleNetLegacy_Xbb + fatjets[event.index_gFatJets[0]].particleNetLegacy_QCD)
			self.out.fillBranch("Fatjet_pnet_bbvsqcd",Fatjet_pnet_bbvsqcd)		

			if(Fatjet_pnet_bbvsqcd>self.pnetloose):
				self.out.fillBranch("hbbloose",1)
				if ((search("Radion",self.filename) or search("Graviton",self.filename)) and (self.isMC) and (abs(fatjets[event.index_gFatJets[0]].hadronFlavour)==5)):
					if((fatjets[event.index_gFatJets[0]].pt_nom>=200) and (fatjets[event.index_gFatJets[0]].pt_nom<250)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt200to250']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt200to250']['final']['central']+self.jsonInfo['LP_pt200to250']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt200to250']['final']['central']-self.jsonInfo['LP_pt200to250']['final']['low'])				

					elif((fatjets[event.index_gFatJets[0]].pt_nom>=250) and (fatjets[event.index_gFatJets[0]].pt_nom<300)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt250to300']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt250to300']['final']['central']+self.jsonInfo['LP_pt250to300']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt250to300']['final']['central']-self.jsonInfo['LP_pt250to300']['final']['low'])

					elif((fatjets[event.index_gFatJets[0]].pt_nom>=300) and (fatjets[event.index_gFatJets[0]].pt_nom<350)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt300to350']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt300to350']['final']['central']+self.jsonInfo['LP_pt300to350']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt300to350']['final']['central']-self.jsonInfo['LP_pt300to350']['final']['low'])


					elif((fatjets[event.index_gFatJets[0]].pt_nom>=350) and (fatjets[event.index_gFatJets[0]].pt_nom<400)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt350to400']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt350to400']['final']['central']+self.jsonInfo['LP_pt350to400']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt350to400']['final']['central']-self.jsonInfo['LP_pt350to400']['final']['low'])

					elif((fatjets[event.index_gFatJets[0]].pt_nom>=400) and (fatjets[event.index_gFatJets[0]].pt_nom<450)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt400to450']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt400to450']['final']['central']+self.jsonInfo['LP_pt400to450']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt400to450']['final']['central']-self.jsonInfo['LP_pt400to450']['final']['low'])

					elif((fatjets[event.index_gFatJets[0]].pt_nom>=450) and (fatjets[event.index_gFatJets[0]].pt_nom<500)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt450to500']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt450to500']['final']['central']+self.jsonInfo['LP_pt450to500']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt450to500']['final']['central']-self.jsonInfo['LP_pt450to500']['final']['low'])


					elif((fatjets[event.index_gFatJets[0]].pt_nom>=500) and (fatjets[event.index_gFatJets[0]].pt_nom<600)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt500to600']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt500to600']['final']['central']+self.jsonInfo['LP_pt500to600']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt500to600']['final']['central']-self.jsonInfo['LP_pt500to600']['final']['low'])

					elif((fatjets[event.index_gFatJets[0]].pt_nom>=600)):
						self.out.fillBranch("hbblooseWeight",self.jsonInfo['LP_pt600to100000']['final']['central'])
						self.out.fillBranch("hbblooseWeightUp",self.jsonInfo['LP_pt600to100000']['final']['central']+self.jsonInfo['LP_pt600to100000']['final']['high'])
						self.out.fillBranch("hbblooseWeightDown",self.jsonInfo['LP_pt600to100000']['final']['central']-self.jsonInfo['LP_pt600to100000']['final']['low'])
				else:
					if (self.isMC):
						self.out.fillBranch("hbblooseWeight",1.0)
						self.out.fillBranch("hbblooseWeightUp",1.0)
						self.out.fillBranch("hbblooseWeightDown",1.0)						
			else:
				self.out.fillBranch("hbbloose",0)
				if(self.isMC):
					self.out.fillBranch("hbblooseWeight",-999.0)
					self.out.fillBranch("hbblooseWeightUp",-999.0)
					self.out.fillBranch("hbblooseWeightDown",-999.0)
		else:
			print("Number of Fatjets in..Nominal...is ZERO")
			self.out.fillBranch("Fatjet_pnet_bbvsqcd",-1.00)
			self.out.fillBranch("hbbloose",0)
			self.out.fillBranch("hbblooseWeight",-999.0)
			self.out.fillBranch("hbblooseWeightUp",-999.0)
			self.out.fillBranch("hbblooseWeightDown",-999.0)			

		if not self.runNominal:
			for sys in self.jesUnc:
				#print("printing the length of the Fatjet for sys = ",sys,"..number of good fatjets = ",getAK8coll(sys)[0],"..and indices..",getAK8coll(sys)[1])
				if (getAK8coll(sys)[0]>0):
					#First fill the mass branches
					self.out.fillBranch("softdropmass%s"%(sys),fatjets[getAK8coll(sys)[1][0]].msoftdrop)
					self.out.fillBranch("softdropmassnom%s"%(sys),fatjets[getAK8coll(sys)[1][0]].msoftdrop_nom)
					self.out.fillBranch("pnetmass%s"%(sys),fatjets[getAK8coll(sys)[1][0]].particleNetLegacy_mass)

					#Proceed with the rest of the branches
					Fatjet_pnet_bbvsqcd = (fatjets[getAK8coll(sys)[1][0]].particleNetLegacy_Xbb)/(fatjets[getAK8coll(sys)[1][0]].particleNetLegacy_Xbb + fatjets[getAK8coll(sys)[1][0]].particleNetLegacy_QCD)
					self.out.fillBranch("Fatjet_pnet_bbvsqcd%s"%(sys),Fatjet_pnet_bbvsqcd)

					if(Fatjet_pnet_bbvsqcd>self.pnetloose):
						self.out.fillBranch("hbbloose%s"%(sys),1)
						if ((search("Radion",self.filename) or search("Graviton",self.filename)) and (self.isMC) and (abs(fatjets[getAK8coll(sys)[1][0]].hadronFlavour)==5)):
							if((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=200) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<250)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt200to250']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=250) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<300)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt250to300']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=300) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<350)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt300to350']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=350) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<400)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt350to400']['final']['central'])


							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=400) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<450)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt400to450']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=450) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<500)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt450to500']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=500) and (getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)<600)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt500to600']['final']['central'])

							elif((getjetpt(fatjets[getAK8coll(sys)[1][0]],sys)>=600)):
								self.out.fillBranch("hbblooseWeight%s"%(sys),self.jsonInfo['LP_pt600to100000']['final']['central'])
						else:
							if (self.isMC):
								self.out.fillBranch("hbblooseWeight%s"%(sys),1.0)				
					else:
						self.out.fillBranch("hbbloose%s"%(sys),0)
						if(self.isMC):
							self.out.fillBranch("hbblooseWeight%s"%(sys),-999.0)
				else:
					#print("Index of nominal fatjet = ",event.index_gFatJets)
					#if(len(fatjets)>1):
					#print("MET = ",getMETpt(sys),"MET_nominal",getMETpt(""),"..FatJet_pt..",getjetpt(fatjets[event.index_gFatJets[0]],sys),"..FatJet_pt Nominal[0]..",getjetpt(fatjets[0],""),fatjets[0].eta,fatjets[0].jetId,"..FatJet_pt Nominal[1]..",getjetpt(fatjets[1],""),fatjets[1].eta,fatjets[1].jetId,"..FatJet_pt Nominal[2]..",getjetpt(fatjets[2],""),fatjets[2].eta,fatjets[2].jetId)
						#print("MET = ",getMETpt(sys),"MET_nominal",getMETpt(""),"..FatJet_pt..",getjetpt(fatjets[event.index_gFatJets[0]],sys),"..FatJet_pt Nominal[0]..",getjetpt(fatjets[0],""),fatjets[0].eta,fatjets[0].jetId,"..FatJet_pt Nominal[1]..",getjetpt(fatjets[1],""),fatjets[1].eta,fatjets[1].jetId)
					#print("MET = ",getMETpt(sys),"MET_nominal",getMETpt(""),"..FatJet_pt..",getjetpt(fatjets[event.index_gFatJets[0]],sys),"..FatJet_pt Nominal[0]..",getjetpt(fatjets[0],""),fatjets[0].eta,fatjets[0].jetId,)					
					#print("Number of Fatjets in..",sys,"...is ZERO,",getAK8coll(sys)[0],getAK8coll(sys)[1],getAK8coll(sys)[1].GetSize())
					self.out.fillBranch("Fatjet_pnet_bbvsqcd%s"%(sys),-1.00)
					self.out.fillBranch("hbbloose%s"%(sys),0)
					self.out.fillBranch("hbblooseWeight%s"%(sys),-999.0)
					self.out.fillBranch("softdropmass%s"%(sys),-1.0)
					self.out.fillBranch("softdropmassnom%s"%(sys),-1.0)
					self.out.fillBranch("pnetmass%s"%(sys),-1.0)


		return True		
		


def call_postpoc(files):
	nameStrip=files.strip()
	filename = (nameStrip.split('/')[-1]).split('.')[-2]
	print(filename)
	
	if (search("Run", filename)):
		print ("This is a ",args.year," Data file = ",filename)
		mainModule = lambda: WeightsAndAssociatedSystematics(filename,args.year,True,args.runNominal)
	else:
		print ("This is a ",args.year," MC file = ", filename)
		mainModule = lambda: WeightsAndAssociatedSystematics(filename,args.year,False,args.runNominal)
	
	p = PostProcessor(args.tempStore,[files], cut=None, branchsel=None,modules=[mainModule()], postfix="",noOut=False,outputbranchsel=None)
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
	fnames = glob.glob(args.inputLocation + "/*MET*.root")

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