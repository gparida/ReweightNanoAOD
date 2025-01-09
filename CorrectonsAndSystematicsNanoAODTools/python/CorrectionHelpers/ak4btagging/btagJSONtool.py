from .helper import modulepath, ensureTFile, warning
from array import array
import ROOT
from correctionlib import _core
import os

path = modulepath

jsonPath = os.environ['CMSSW_BASE'] + '/src/jsonpog-integration/POG/BTV/'


class BTagWPs:
	"""Contain b tagging working points."""
	def __init__( self, tagger, year=2016 ):
		assert( year in ["2016","2016APV","2017","2018"] ), "You must choose a year from: 2016, 2016APV, 2017, or 2018."
		if year=="2016":
			if 'deepjetflavb' in tagger.lower():
				self.loose    = 0.0480 
				self.medium   = 0.2489 
				self.tight    = 0.6377 

		elif year=="2016APV":
			if 'deepjetflavb' in tagger.lower():
				self.loose    = 0.0508 
				self.medium   = 0.2598
				self.tight    = 0.6502

		elif year=="2017":
			if 'deepjetflavb' in tagger.lower():
				self.loose    = 0.0532 
				self.medium   = 0.3040
				self.tight    = 0.7476

		elif year=="2018":
			if 'deepjetflavb' in tagger.lower():
				self.loose    = 0.0490
				self.medium   = 0.2783
				self.tight    = 0.7100
	
class BTagWeightTool:
		
		def __init__(self, tagger, wp, sigmabc='central', sigmalight='central', year=2016):
				"""Load b tag weights from CSV file."""
				
				assert(year in ["2016","2016APV","2017","2018"]), "You must choose a year from: 2016, 2016APV, 2017, or 2018."
				assert(tagger in ['deepjetflavb']), "BTagWeightTool: You must choose a tagger from: deepjetflavb!"
				assert(wp in ['loose','medium','tight']), "BTagWeightTool: You must choose a WP from: loose, medium, tight!"
				
				self.sigmabc = sigmabc
				self.sigmalight = sigmalight
				# FILE
				if year=="2016":
					self.year_unc = "2016"
					if 'deepjetflavb' in tagger.lower():
						correctionJSON = jsonPath +'/2016postVFP_UL/btagging.json.gz'
						#effname = path +'/'+year+'/DeepJetFlavB_2016_eff_'+wp.upper()+'.root'
						#effname = path +'/'+'AK8ScoreOrderingFiles'+'/'+year+'/DeepJetFlavB_2016_eff_'+wp.upper()+'.root'
						effname = path +'/'+'AK8PtOrdering_pt200_Files'+'/'+year+'/DeepJetFlavB_2016_eff_'+wp.upper()+'.root'
						
				if year=="2016APV":
					self.year_unc = "2016"
					if 'deepjetflavb' in tagger.lower():
						correctionJSON = jsonPath +'/2016preVFP_UL/btagging.json.gz'
						#effname = path +'/'+year+'/DeepJetFlavB_2016APV_eff_'+wp.upper()+'.root'
						#effname =  path +'/'+'AK8ScoreOrderingFiles'+'/'+year+'/DeepJetFlavB_2016APV_eff_'+wp.upper()+'.root'
						effname =  path +'/'+'AK8PtOrdering_pt200_Files'+'/'+year+'/DeepJetFlavB_2016APV_eff_'+wp.upper()+'.root'

				elif year=="2017":
					self.year_unc = "2017"
					if 'deepjetflavb' in tagger.lower():
						correctionJSON = jsonPath +'/2017_UL/btagging.json.gz'
						#effname = path +'/'+year+'/DeepJetFlavB_2017_eff_'+wp.upper()+'.root'
						#effname = path +'/'+'AK8ScoreOrderingFiles'+'/'+year+'/DeepJetFlavB_2017_eff_'+wp.upper()+'.root'
						effname = path +'/'+'AK8PtOrdering_pt200_Files'+'/'+year+'/DeepJetFlavB_2017_eff_'+wp.upper()+'.root'
 
				elif year=="2018":
					self.year_unc = "2018"
					if 'deepjetflavb' in tagger.lower():
						correctionJSON = jsonPath +'/2018_UL/btagging.json.gz'
						#effname = path +'/'+year+'/DeepJetFlavB_2018_eff_'+wp.upper()+'.root'
						#effname =  path +'/'+'AK8ScoreOrderingFiles'+'/'+year+'/DeepJetFlavB_2018_eff_'+wp.upper()+'.root'
						effname =  path +'/'+'/'+year+'/DeepJetFlavB_2018_eff_'+wp.upper()+'.root'
				# TAGGING WP
				self.evaluator = _core.CorrectionSet.from_file(correctionJSON)
				self.wpname = wp
				self.wp     = getattr(BTagWPs(tagger,year),wp)
				if 'deepjetflavb' in tagger.lower():
					tagged = lambda j: j.btagDeepFlavB>self.wp

				
				# EFFICIENCIES
				effmaps    = { } # b tag efficiencies in MC to compute b tagging weight for an event
				efffile    = ensureTFile(effname)
				default    = False
				if not efffile:
					warning("File %s with efficiency histograms does not exist! Reverting to crying..."%(effname),title="BTagWeightTool")
					default  = True
				for flavor in [0,4,5]:
					flavor   = flavorToString(flavor)
					#histname = "%s_%s_%s"%(tagger,flavor,wp)
					effname  = "%s/eff_%s_%s_%s"%(year,"DeepJetFlavB",flavor,wp)
					if efffile:
						effmaps[flavor]    = efffile.Get(effname)
						if not effmaps[flavor]:
							warning("histogram '%s' does not exist in %s! Reverting to crying..."%(effname,efffile.GetName()),title="BTagWeightTool")
					else:
							warning("histogram '%s' does not exist in %s! Reverting to crying..."%(effname,efffile.GetName()),title="BTagWeightTool")
					effmaps[flavor].SetDirectory(0)
				efffile.Close()
				
				if default:
					warning("Made use of crying! The b tag weights from this module should be regarded as placeholders only,\n"+\
									"and should NOT be used for analyses. B (mis)tag efficiencies in MC are analysis dependent. Please create your own\n"+\
									"efficiency histogram with corrections/btag/getBTagEfficiencies.py after running all MC samples with BTagWeightTool.",title="BTagWeightTool")
				
				self.tagged  = tagged
				self.effmaps = effmaps

		def getjetpt(self, jet, sys):
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

		def getWeight(self,jetCollection,sys):
				weight = 1.
				for jet in jetCollection:
						weight *= self.getSF(jet,sys)
				return weight
				
		def getSF(self,jet,sys):
				"""Get b tag SF for a single jet."""
				#pt = jet.pt_nom
				#eta = jet.eta
				#flavor = jet.hadronFlavour
				#Sanity check
				#print("In get SF func, for..",sys,"...Jet pt = ",self.getjetpt(jet,sys),"..abs(eta)..",abs(jet.eta),"...flav..",jet.hadronFlavour)
				if jet.hadronFlavour == 0:
					#SF   = self.evaluator["deepJet_incl"].evaluate(self.sigmalight,self.wpname.upper()[:1],flavor,abs(eta),pt) # self.wpname.upper()[:1] --- Convert loose to LOOSE and pick the L. Simillarly for other WPs
					SF   = self.evaluator["deepJet_incl"].evaluate(self.sigmalight,self.wpname.upper()[:1],jet.hadronFlavour,abs(jet.eta),self.getjetpt(jet,sys)) # self.wpname.upper()[:1] --- Convert loose to LOOSE and pick the L. Simillarly for other WPs
				else:
					#SF   = self.evaluator["deepJet_comb"].evaluate(self.sigmabc,self.wpname.upper()[:1],flavor,abs(eta),pt) # self.wpname.upper()[:1] --- Convert loose to LOOSE and pick the L. Simillarly for other WPs
					SF   = self.evaluator["deepJet_comb"].evaluate(self.sigmabc,self.wpname.upper()[:1],jet.hadronFlavour,abs(jet.eta),self.getjetpt(jet,sys)) # self.wpname.upper()[:1] --- Convert loose to LOOSE and pick the L. Simillarly for other WPs
				tagged = self.tagged(jet)
				if tagged:
					weight = SF
					#print(">>"+self.wpname+"_tagged>>"+">>flav_ = "+str(flavor)+">>Pt_ = "+str(pt)+">>Eta_ = "+str(eta)+">>Weight_ = "+str(weight))
				else:
					#eff = self.getEfficiency(pt,eta,flavor)
					eff = self.getEfficiency(self.getjetpt(jet,sys),jet.eta,jet.hadronFlavour)
					if eff==1:
						#print ("Warning! BTagWeightTool.getSF: MC efficiency is 1 for pt=%s, eta=%s, flavor=%s, SF=%s"%(pt,eta,flavor,SF))
						return 1
					else:
						weight = (1-SF*eff)/(1-eff)
					#print(">>"+self.wpname+"_NOTtagged>>"+">>flav_ = "+str(flavor)+">>Pt_ = "+str(pt)+">>Eta_ = "+str(eta)+">>Weight_ = "+str(weight))
				return weight
				
		def getEfficiency(self,pt,eta,flavor):
				"""Get b tag efficiency for a single jet in MC."""
				flavor = flavorToString(flavor)
				hist   = self.effmaps[flavor]
				xbin   = hist.GetXaxis().FindBin(pt)
				ybin   = hist.GetYaxis().FindBin(eta)
				if xbin==0: xbin = 1
				elif xbin>hist.GetXaxis().GetNbins(): xbin -= 1
				if ybin==0: ybin = 1
				elif ybin>hist.GetYaxis().GetNbins(): ybin -= 1
				eff    = hist.GetBinContent(xbin,ybin)
				#if eff==1:
				#  print "Warning! BTagWeightTool.getEfficiency: MC efficiency is 1 for pt=%s, eta=%s, flavor=%s, SF=%s"%(pt,eta,flavor,SF)
				return eff
		 


def flavorToFLAV(flavor):
	"""Help function to convert an integer flavor ID to a BTagEntry enum value."""
	#return FLAV_B if abs(flavor)==5 else FLAV_C if abs(flavor) in [4,15] else FLAV_UDSG     
	return FLAV_B if abs(flavor)==5 else FLAV_C if abs(flavor)==4 else FLAV_UDSG       

	
def flavorToString(flavor):
	"""Help function to convert an integer flavor ID to a string value."""
	return 'b' if abs(flavor)==5 else 'c' if abs(flavor)==4 else 'udsg'
	
