import ROOT

def CalculateTauIDWeight(self,theTree):
    self.value[0] = 1.0
    #for tau in range(len(theTree.allTau_pt)):
    #    tauVector =  ROOT.TLorentzVector()
    #    tauVector.SetPtEtaPhiM(theTree.allTau_pt[tau],theTree.allTau_eta[tau],theTree.allTau_phi[tau],theTree.allTau_mass[tau])
    #    print ("pt value that is passed = ", tauVector.Pt(),theTree.allTau_genPartFlav[tau])
    #    self.value[0] = self.value[0] * self.SFTool.getSFvsPT(tauVector.Pt(),genmatch=theTree.allTau_genPartFlav[tau])
        
    for tau in range(len(theTree.gboostedTau_pt)):
        tauVector =  ROOT.TLorentzVector()
        tauVector.SetPtEtaPhiM(theTree.gboostedTau_pt[tau],theTree.gboostedTau_eta[tau],theTree.gboostedTau_phi[tau],theTree.gboostedTau_mass[tau])
        print ("pt value that is passed = ", tauVector.Pt(),theTree.gboostedTau_genPartFlav[tau])
        self.value[0] = self.value[0] * self.SFTool_boosted.getSFvsPT(tauVector.Pt(),genmatch=theTree.gboostedTau_genPartFlav[tau])
    
    for tau in range(len(theTree.gTau_pt)):
        tauVector =  ROOT.TLorentzVector()
        tauVector.SetPtEtaPhiM(theTree.gTau_pt[tau],theTree.gTau_eta[tau],theTree.gTau_phi[tau],theTree.gTau_mass[tau])
        print ("pt value that is passed = ", tauVector.Pt(),theTree.gTau_genPartFlav[tau])
        self.value[0] = self.value[0] * self.SFTool_standard.getSFvsPT(tauVector.Pt(),genmatch=theTree.gTau_genPartFlav[tau])