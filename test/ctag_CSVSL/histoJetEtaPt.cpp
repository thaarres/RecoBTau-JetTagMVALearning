#include <TFile.h>
#include <TH2D.h>
#include <vector>
#include <TString.h>
#include <TChain.h>
#include <TDirectory.h>

#include <stdio.h>
#include <iostream> // for std::cout and std::endl

void paint(TString dir, TString a, TString b)
{
	TChain *t = new TChain(a);
	t->Add(dir + a + "_" + b +".root");

	std::cout << "painting the histograms for: " << dir + a + "_" + b +".root" << std::endl;

	TDirectory *direc = new TDirectory("dir", "dir");
	direc->cd();

	TH2D * histo = new TH2D("jets", "jets", 50, -2.5, 2.5, 40, 4.17438727, 6.95654544315);//pt starting from 15 and until 1000
	histo->SetDirectory(direc);

	t->Draw("log(jetPt+50):jetEta >> +jets", "", "Lego goff");

  TH2D * histo_lin = new TH2D("jets_lin", "jets_lin", 50, -2.5, 2.5, 40, 15, 1000);//pt starting from 15 and until 1000
	t->Draw("jetPt:jetEta >> +jets_lin", "", "Lego goff");

	std::cout << "saving the histograms: " << a + "_" + b +"_histo.root" << std::endl;
	TFile g(a + "_" + b +"_histo.root", "RECREATE");
	histo->SetDirectory(&g);
	histo_lin->SetDirectory(&g);
	delete direc;

	g.cd();
	histo->Write();
	histo_lin->Write();
	g.Close();

}

int main(int argc, char **argv)
{
	TString dir = "";
	TString fix = "";
	if(argc == 2 || argc == 3) dir = TString(argv[1])+"skimmed_20k_eachptetabin_";
	if(argc == 3) fix = argv[2];

	std::cout << "reading rootfiles from directory " << dir << std::endl;
	
  std::vector<TString> cat;
  cat.push_back(fix+"RecoVertexNoSoftLepton");
  cat.push_back(fix+"PseudoVertexNoSoftLepton");
  cat.push_back(fix+"NoVertexNoSoftLepton");
  cat.push_back(fix+"RecoVertexSoftElectron");
  cat.push_back(fix+"PseudoVertexSoftElectron");
  cat.push_back(fix+"NoVertexSoftElectron");
  cat.push_back(fix+"RecoVertexSoftMuon");
  cat.push_back(fix+"PseudoVertexSoftMuon");
  cat.push_back(fix+"NoVertexSoftMuon");
  std::vector<TString> types;
  types.push_back("DUSG");
  types.push_back("C");
  types.push_back("B");
  for(size_t i=0;i< cat.size(); i++){
   for(size_t j=0;j< types.size(); j++){
	  paint(dir,cat[i],types[j]);
   }
 }
 
 return 0;

}
