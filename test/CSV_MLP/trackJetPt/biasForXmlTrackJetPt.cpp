//I add 2 extra high pt bins: 400 < PT < 600; PT>600 GeV
//For those I only use 2 eta bins

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "TString.h"
#include "TTree.h"
#include "TFile.h"
#include "TROOT.h"
#include "TObject.h"

using namespace std;

// define name Tree in calcEntries()

void calcEntries(string  flavour, string category, vector<float> & entries, string dir, string fix);

int main(int argc, char **argv){

	string dir = "/afs/cern.ch/work/p/pvmulder/public/BTagging/GIT_SETUP/TEST_RECIPE/CMSSW_5_3_13_patch3/src/RootFiles_CMSSW5313_gitrecipe/TT_biases";
	string fix = "CombinedSV";

	if(argc == 2 || argc == 3) dir = argv[1];
	if(argc == 3) fix = argv[2];
		
	cout << "calculate bias from rootfiles in dir " << dir << endl;

	string flavour[3] = {"B", "C", "DUSG"};
	string cat[3] = {"NoVertex", "PseudoVertex", "RecoVertex"};

	vector<float> entries[9];

	int nIter =0;

	for(int j=0; j<3; j++){//loop on categories
		for(int i =0; i<3; i++){//loop on flavours
			calcEntries(flavour[i], cat[j], entries[nIter], dir, fix);
			nIter++;
		}
	}


  ofstream myfile;
	string filename = "";
	for(int j=0; j<3; j++){//loop on categories	
		for(int k=1; k<3; k++){//loop on C and light
			cout<<"***************   "<<cat[j]<<"_B_"<<flavour[k]<<"   ***************"<<endl;
			filename = cat[j]+"_B_"+flavour[k]+".txt";
  		myfile.open (filename.c_str());
 			for(int l = 0; l<19; l++ ){// loop on pt/eta bins defined in xml
 			//for(int l = 0; l<1; l++ ){// loop on pt/eta bins defined in xml
				int index = j*3;
				int indexb = k+j*3;
				float bias = (float)((entries[index][l]/(entries[0][l]+entries[3][l]+entries[6][l]))/((entries[indexb][l]/(entries[k][l]+entries[k+3][l]+entries[k+6][l]))));
  			myfile << "<bias>"<<bias<<"</bias>\n";
				cout<<"<bias>"<<bias<<"</bias>"<<endl; 
			}
			myfile.close();
		}
	}
	
	return 0;
}


void calcEntries(string flavour, string  category,  vector<float> & entries, string dir, string fix){	
	TFile * f = TFile::Open((dir+"/"+fix+category+"_"+flavour+".root").c_str());
  
	cout << "opening file: " << (dir+"/"+fix+category+"_"+flavour+".root").c_str() << endl;
	   
	f->cd();
	TTree * t =(TTree*)f->Get((fix+category).c_str());

	//definition of pt and eta bins should be the same as in the Train*xml files!!!
//	entries.push_back(t->GetEntries());
	entries.push_back(t->GetEntries("trackJetPt>0&&trackJetPt<40&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>0&&trackJetPt<40&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>0&&trackJetPt<40&&(!(TMath::Abs(jetEta)<2.1))"));
	entries.push_back(t->GetEntries("trackJetPt>40&&trackJetPt<60&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>40&&trackJetPt<60&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>40&&trackJetPt<60&&(!(TMath::Abs(jetEta)<2.1))"));
	entries.push_back(t->GetEntries("trackJetPt>60&&trackJetPt<90&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>60&&trackJetPt<90&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>60&&trackJetPt<90&&(!(TMath::Abs(jetEta)<2.1))"));
	entries.push_back(t->GetEntries("trackJetPt>90&&trackJetPt<150&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>90&&trackJetPt<150&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>90&&trackJetPt<150&&(!(TMath::Abs(jetEta)<2.1))"));
	entries.push_back(t->GetEntries("trackJetPt>150&&trackJetPt<400&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>150&&trackJetPt<400&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>150&&trackJetPt<400&&(!(TMath::Abs(jetEta)<2.1))"));
	entries.push_back(t->GetEntries("trackJetPt>400&&trackJetPt<600&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>400&&trackJetPt<600&&(!(TMath::Abs(jetEta)<1.2))"));
	entries.push_back(t->GetEntries("trackJetPt>600&&TMath::Abs(jetEta)<1.2"));
	entries.push_back(t->GetEntries("trackJetPt>600&&(!(TMath::Abs(jetEta)<1.2))"));

	cout << "jets have been put in pt and eta bins now" << endl;
	    
}



