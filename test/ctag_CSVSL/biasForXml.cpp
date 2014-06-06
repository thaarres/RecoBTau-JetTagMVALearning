// g++ biasForXml.cpp `root-config --cflags --glibs` -o bias
// ./bias $path_to_rootfiles $prefix
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
	string dir = "/gpfs/cms/users/umer/CMSSW_5_3_16/src/work/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/TTbar_biases";
	string fix = "CombinedSV";

	if(argc == 2 || argc == 3) dir = argv[1];
	if(argc == 3) fix = argv[2];
		
	cout << "calculate bias from rootfiles in dir " << dir << endl;

	string flavour[3] = {"C", "B", "DUSG"};
	string cat[9] = {"NoVertexNoSoftLepton", "PseudoVertexNoSoftLepton", "RecoVertexNoSoftLepton", "NoVertexSoftElectron", "PseudoVertexSoftElectron", "RecoVertexSoftElectron","NoVertexSoftMuon", "PseudoVertexSoftMuon", "RecoVertexSoftMuon"};

	vector<float> entries[27];

	int nIter =0;

	for(int j=0; j<9; j++){//loop on categories
		for(int i =0; i<3; i++){//loop on flavours
			calcEntries(flavour[i], cat[j], entries[nIter], dir, fix);
			//for(int k =0 ; k<entries[nIter].size(); k++) cout<<flavour[i]<<"   "<<cat[j]<<"  "<<entries[nIter][k]<<endl; 
			nIter++;
		}
	}

	int count = 0;
	for(int j=0; j<9; j++){//loop on categories
		for(int i =0; i<3; i++){//loop on flavours
			cout << "for category " << cat[j] << " and jet flavour " << flavour[i] << " there are " << entries[count][0] << " entries"  << endl;
			count++;
		}
	}
	cout << "for jet flavour C there are " << entries[0][0]+entries[3][0]+entries[6][0]+entries[9][0]+entries[12][0]+entries[15][0]+entries[18][0]+entries[21][0]+entries[24][0]<< " entries"  << endl;
	cout << "for jet flavour B there are " << entries[1][0]+entries[4][0]+entries[7][0]+entries[10][0]+entries[13][0]+entries[16][0]+entries[19][0]+entries[22][0]+entries[25][0] << " entries"  << endl;
	cout << "for jet flavour DUSG there are " << entries[2][0]+entries[5][0]+entries[8][0]+entries[11][0]+entries[14][0]+entries[17][0]+entries[20][0]+entries[23][0]+entries[26][0] << " entries"  << endl;

  ofstream myfile;
	string filename = "";
	for(int j=0; j<9; j++){//loop on categories	
		for(int k=1; k<3; k++){//loop on B and light
			cout<<"***************   "<<cat[j]<<"_C_"<<flavour[k]<<"   ***************"<<endl;
			filename = cat[j]+"_C_"+flavour[k]+".txt";
  		myfile.open (filename.c_str());
 			for(int l = 0; l<19; l++ ){// loop on pt/eta bins defined in xml
 			//for(int l = 0; l<1; l++ ){// loop on pt/eta bins defined in xml
				int index = j*3;
				int indexb = k+j*3;
				float bias = (float)((entries[index][l]/(entries[0][l]+entries[3][l]+entries[6][l]+entries[9][0]+entries[12][0]+entries[15][0]+entries[18][0]+entries[21][0]+entries[24][0]))/((entries[indexb][l]/(entries[k][l]+entries[k+3][l]+entries[k+6][l]+entries[k+9][l]+entries[k+12][l]+entries[k+15][l]+entries[k+18][l]+entries[k+21][l]+entries[k+24][l]))));
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
	entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>15&&jetPt<40&&|jetEta|<1.2: " << t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>15&&jetPt<40&&1.2<|jetEta|<2.1: " << t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&(!(TMath::Abs(jetEta)<2.1))"));
	cout << "jetPt>15&&jetPt<40&&2.1<|jetEta|<2.4: " << t->GetEntries("jetPt>15&&jetPt<40&&(!(TMath::Abs(jetEta)<2.1))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>40&&jetPt<60&&|jetEta|<1.2: " << t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>40&&jetPt<60&&1.2<|jetEta|<2.1: " << t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&(!(TMath::Abs(jetEta)<2.1))"));
	cout << "jetPt>40&&jetPt<60&&2.1<|jetEta|<2.4: " << t->GetEntries("jetPt>40&&jetPt<60&&(!(TMath::Abs(jetEta)<2.1))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>60&&jetPt<90&&|jetEta|<1.2: " << t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>60&&jetPt<90&&1.2<|jetEta|<2.1: " << t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&(!(TMath::Abs(jetEta)<2.1))"));
	cout << "jetPt>60&&jetPt<90&&2.1<|jetEta|<2.4: " << t->GetEntries("jetPt>60&&jetPt<90&&(!(TMath::Abs(jetEta)<2.1))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>90&&jetPt<150&&|jetEta|<1.2: " << t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>90&&jetPt<150&&1.2<|jetEta|<2.1: " << t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&(!(TMath::Abs(jetEta)<2.1))"));
	cout << "jetPt>90&&jetPt<150&&2.1<|jetEta|<2.4: " << t->GetEntries("jetPt>90&&jetPt<150&&(!(TMath::Abs(jetEta)<2.1))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>150&&jetPt<400&&|jetEta|<1.2: " << t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>150&&jetPt<400&&1.2<|jetEta|<2.1: " << t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&(!(TMath::Abs(jetEta)<2.1))"));
	cout << "jetPt>150&&jetPt<400&&2.1<|jetEta|<2.4: " << t->GetEntries("jetPt>150&&jetPt<400&&(!(TMath::Abs(jetEta)<2.1))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>400&&jetPt<600&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>400&&jetPt<600&&|jetEta|<1.2: " << t->GetEntries("jetPt>400&&jetPt<600&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>400&&jetPt<600&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>400&&jetPt<600&&1.2<|jetEta|<2.4: " << t->GetEntries("jetPt>400&&jetPt<600&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>600&&TMath::Abs(jetEta)<1.2"));
	cout << "jetPt>600&&|jetEta|<1.2: " << t->GetEntries("jetPt>600&&TMath::Abs(jetEta)<1.2") << " jets" << endl;
	entries.push_back(t->GetEntries("jetPt>600&&(!(TMath::Abs(jetEta)<1.2))"));
	cout << "jetPt>600&&1.2<|jetEta|<2.4: " << t->GetEntries("jetPt>600&&(!(TMath::Abs(jetEta)<1.2))") << " jets" << endl;

	    
}



