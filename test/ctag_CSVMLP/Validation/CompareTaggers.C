// general
#include "TH1.h"
#include "TH2F.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TSystem.h"
#include "TF1.h"
#include "TKey.h"
#include "TH1F.h"
#include "TStyle.h"
#include "TProfile.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TLine.h"
#include "TArrow.h"
#include "TLatex.h"
#include "TMinuit.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TFormula.h"
#include "TAxis.h"

#include <iostream.h>
#include <stdio.h>
#include <fstream.h>
#include <vector.h>
#include "./tdrstyle.C"

TFile *file1;
TLegend *leg;
string plotname;

void CompareTaggers()
{
  using namespace std;

  setTDRStyle();
  gStyle->SetOptFit(0);
  gStyle->SetOptStat(0);
  
	string dir = "PlotsEvaluation_categories";
	
	gSystem->mkdir(dir.c_str());

	TString fileName1 = "DQM_V0001_R000000001__POG__BTAG__ttincl.root";
	file1 = TFile::Open(fileName1);

	TString fileNameVish = "DQM_standard_CSVLRctag.root";
	file2 = TFile::Open(fileNameVish);

	TString fileNameVish2 = "DQM_standard_CSVV2ctag.root";
	file3 = TFile::Open(fileNameVish2);

	TString fileName2 = "/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/SuperTaggerDev/JetFlavourPUjetID/CMSSW_5_3_14/src/RecoBTau/JetTagMVALearning/test/CSVSL/Validation/DQM_V0001_R000000001__POG__BTAG__allTaggers_20140325_selTracksALLminMult2.root";
	file4 = TFile::Open(fileName2);

	TString fileName3 = "DQM_V0001_R000000001__POG__BTAG__tthad.root";
	file5 = TFile::Open(fileName3);

	if (!file1) abort();

	TH1F * oldCSVIVF_effB = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/oldCSVIVF_GLOBAL/effVsDiscrCut_discr_oldCSVIVF_GLOBALB");
	TH1F * oldCSVIVF_effC = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/oldCSVIVF_GLOBAL/effVsDiscrCut_discr_oldCSVIVF_GLOBALC");
	TH1F * oldCSVIVF_effDUSG = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/oldCSVIVF_GLOBAL/effVsDiscrCut_discr_oldCSVIVF_GLOBALDUSG");

	TH1F * CSVIVFV2_effB = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFV2_GLOBAL/effVsDiscrCut_discr_CSVIVFV2_GLOBALB");
	TH1F * CSVIVFV2_effC = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFV2_GLOBAL/effVsDiscrCut_discr_CSVIVFV2_GLOBALC");
	TH1F * CSVIVFV2_effDUSG = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFV2_GLOBAL/effVsDiscrCut_discr_CSVIVFV2_GLOBALDUSG");
	
	TH1F * CSVIVFSL_effB = (TH1F*) file4->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSL_GLOBAL/effVsDiscrCut_discr_CSVIVFSL_GLOBALB");
	TH1F * CSVIVFSL_effC = (TH1F*) file4->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSL_GLOBAL/effVsDiscrCut_discr_CSVIVFSL_GLOBALC");
	TH1F * CSVIVFSL_effDUSG = (TH1F*) file4->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSL_GLOBAL/effVsDiscrCut_discr_CSVIVFSL_GLOBALDUSG");

	TH1F * CSVLRctag_effB = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALB");
	TH1F * CSVLRctag_effC = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALC");
	TH1F * CSVLRctag_effDUSG = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALDUSG");

	TH1F * CSVV2ctag_effB = (TH1F*) file3->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALB");
	TH1F * CSVV2ctag_effC = (TH1F*) file3->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALC");
	TH1F * CSVV2ctag_effDUSG = (TH1F*) file3->Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/effVsDiscrCut_discr_CSV_GLOBALDUSG");
	
	TH1F * CSVIVFSLctag_effB = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSLctag_GLOBAL/effVsDiscrCut_discr_CSVIVFSLctag_GLOBALB");
	TH1F * CSVIVFSLctag_effC = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSLctag_GLOBAL/effVsDiscrCut_discr_CSVIVFSLctag_GLOBALC");
	TH1F * CSVIVFSLctag_effDUSG = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/CSVIVFSLctag_GLOBAL/effVsDiscrCut_discr_CSVIVFSLctag_GLOBALDUSG");

	//cout << "effB->GetNbinsX()+1: " << effB->GetNbinsX()+1 << endl;
	const Int_t n = 100;
	Double_t oldCSVIVF_C[n], oldCSVIVF_B[n], oldCSVIVF_L[n], oldCSVIVF_eC[n], oldCSVIVF_eB[n], oldCSVIVF_eL[n];
	Double_t CSVIVFV2_C[n], CSVIVFV2_B[n], CSVIVFV2_L[n], CSVIVFV2_eC[n], CSVIVFV2_eB[n], CSVIVFV2_eL[n];
	Double_t CSVIVFSL_C[n], CSVIVFSL_B[n], CSVIVFSL_L[n], CSVIVFSL_eC[n], CSVIVFSL_eB[n], CSVIVFSL_eL[n];
	Double_t CSVLRctag_C[n], CSVLRctag_B[n], CSVLRctag_L[n], CSVLRctag_eC[n], CSVLRctag_eB[n], CSVLRctag_eL[n];
	Double_t CSVV2ctag_C[n], CSVV2ctag_B[n], CSVV2ctag_L[n], CSVV2ctag_eC[n], CSVV2ctag_eB[n], CSVV2ctag_eL[n];
	Double_t CSVIVFSLctag_C[n], CSVIVFSLctag_B[n], CSVIVFSLctag_L[n], CSVIVFSLctag_eC[n], CSVIVFSLctag_eB[n], CSVIVFSLctag_eL[n];
	for(int bin = 0; bin<n; bin++){
		oldCSVIVF_C[bin] = oldCSVIVF_effC->GetBinContent(bin+1);
		oldCSVIVF_B[bin] = oldCSVIVF_effB->GetBinContent(bin+1);
		oldCSVIVF_L[bin] = oldCSVIVF_effDUSG->GetBinContent(bin+1);
		oldCSVIVF_eC[bin] = oldCSVIVF_effC->GetBinError(bin+1);
		oldCSVIVF_eB[bin] = oldCSVIVF_effB->GetBinError(bin+1);
		oldCSVIVF_eL[bin] = oldCSVIVF_effDUSG->GetBinError(bin+1);

		CSVIVFV2_C[bin] = CSVIVFV2_effC->GetBinContent(bin+1);
		CSVIVFV2_B[bin] = CSVIVFV2_effB->GetBinContent(bin+1);
		CSVIVFV2_L[bin] = CSVIVFV2_effDUSG->GetBinContent(bin+1);
		CSVIVFV2_eC[bin] = CSVIVFV2_effC->GetBinError(bin+1);
		CSVIVFV2_eB[bin] = CSVIVFV2_effB->GetBinError(bin+1);
		CSVIVFV2_eL[bin] = CSVIVFV2_effDUSG->GetBinError(bin+1);

		CSVIVFSL_C[bin] = CSVIVFSL_effC->GetBinContent(bin+1);
		CSVIVFSL_B[bin] = CSVIVFSL_effB->GetBinContent(bin+1);
		CSVIVFSL_L[bin] = CSVIVFSL_effDUSG->GetBinContent(bin+1);
		CSVIVFSL_eC[bin] = CSVIVFSL_effC->GetBinError(bin+1);
		CSVIVFSL_eB[bin] = CSVIVFSL_effB->GetBinError(bin+1);
		CSVIVFSL_eL[bin] = CSVIVFSL_effDUSG->GetBinError(bin+1);
	
		CSVLRctag_C[bin] = CSVLRctag_effC->GetBinContent(bin+1);
		CSVLRctag_B[bin] = CSVLRctag_effB->GetBinContent(bin+1);
		CSVLRctag_L[bin] = CSVLRctag_effDUSG->GetBinContent(bin+1);
		CSVLRctag_eC[bin] = CSVLRctag_effC->GetBinError(bin+1);
		CSVLRctag_eB[bin] = CSVLRctag_effB->GetBinError(bin+1);
		CSVLRctag_eL[bin] = CSVLRctag_effDUSG->GetBinError(bin+1);

		CSVV2ctag_C[bin] = CSVV2ctag_effC->GetBinContent(bin+1);
		CSVV2ctag_B[bin] = CSVV2ctag_effB->GetBinContent(bin+1);
		CSVV2ctag_L[bin] = CSVV2ctag_effDUSG->GetBinContent(bin+1);
		CSVV2ctag_eC[bin] = CSVV2ctag_effC->GetBinError(bin+1);
		CSVV2ctag_eB[bin] = CSVV2ctag_effB->GetBinError(bin+1);
		CSVV2ctag_eL[bin] = CSVV2ctag_effDUSG->GetBinError(bin+1);

		CSVIVFSLctag_C[bin] = CSVIVFSLctag_effC->GetBinContent(bin+1);
		CSVIVFSLctag_B[bin] = CSVIVFSLctag_effB->GetBinContent(bin+1);
		CSVIVFSLctag_L[bin] = CSVIVFSLctag_effDUSG->GetBinContent(bin+1);
		CSVIVFSLctag_eC[bin] = CSVIVFSLctag_effC->GetBinError(bin+1);
		CSVIVFSLctag_eB[bin] = CSVIVFSLctag_effB->GetBinError(bin+1);
		CSVIVFSLctag_eL[bin] = CSVIVFSLctag_effDUSG->GetBinError(bin+1);
	
	}
	TCanvas * Plots1 = new TCanvas("Plots1","");
	Plots1->SetLogy();
	Plots1->SetGridx();
	Plots1->SetGridy();
	oldCSVIVF_CvsDUSG = new TGraphErrors(n,oldCSVIVF_C,oldCSVIVF_L,oldCSVIVF_eC,oldCSVIVF_eL);
	oldCSVIVF_CvsDUSG->GetXaxis()->SetTitle("C efficiency");
	//oldCSVIVF_CvsDUSG->GetXaxis()->SetTitleOffset(1.2);
	oldCSVIVF_CvsDUSG->GetXaxis()->SetRangeUser(0,1);
	oldCSVIVF_CvsDUSG->GetYaxis()->SetTitle("DUSG efficiency");
	oldCSVIVF_CvsDUSG->GetYaxis()->SetTitleOffset(1.2);
	oldCSVIVF_CvsDUSG->GetYaxis()->SetRangeUser(0.001,1);
	oldCSVIVF_CvsDUSG->SetTitle("");	
	oldCSVIVF_CvsDUSG->SetMarkerColor(1);
	oldCSVIVF_CvsDUSG->SetMarkerStyle(25);
	oldCSVIVF_CvsDUSG->Draw("AP");	
  
	CSVIVFV2_CvsDUSG = new TGraphErrors(n,CSVIVFV2_C,CSVIVFV2_L,CSVIVFV2_eC,CSVIVFV2_eL);
	CSVIVFV2_CvsDUSG->SetMarkerColor(2);
	CSVIVFV2_CvsDUSG->SetMarkerStyle(24);
	CSVIVFV2_CvsDUSG->Draw("Psame");	

	CSVIVFSL_CvsDUSG = new TGraphErrors(n,CSVIVFSL_C,CSVIVFSL_L,CSVIVFSL_eC,CSVIVFSL_eL);
	CSVIVFSL_CvsDUSG->SetMarkerColor(9);
	CSVIVFSL_CvsDUSG->SetMarkerStyle(29);
//	CSVIVFSL_CvsDUSG->Draw("Psame");	

	CSVLRctag_CvsDUSG = new TGraphErrors(n,CSVLRctag_C,CSVLRctag_L,CSVLRctag_eC,CSVLRctag_eL);
	CSVLRctag_CvsDUSG->SetMarkerColor(6);
	CSVLRctag_CvsDUSG->SetMarkerStyle(27);
	CSVLRctag_CvsDUSG->Draw("Psame");	

	CSVV2ctag_CvsDUSG = new TGraphErrors(n,CSVV2ctag_C,CSVV2ctag_L,CSVV2ctag_eC,CSVV2ctag_eL);
	CSVV2ctag_CvsDUSG->SetMarkerColor(8);
	CSVV2ctag_CvsDUSG->SetMarkerStyle(28);
//	CSVV2ctag_CvsDUSG->Draw("Psame");	

	CSVIVFSLctag_CvsDUSG = new TGraphErrors(n,CSVIVFSLctag_C,CSVIVFSLctag_L,CSVIVFSLctag_eC,CSVIVFSLctag_eL);
	CSVIVFSLctag_CvsDUSG->SetMarkerColor(4);
	CSVIVFSLctag_CvsDUSG->SetMarkerStyle(26);
	CSVIVFSLctag_CvsDUSG->Draw("Psame");	

	leg = new TLegend(0.5,0.2,0.9,0.6);
	leg->SetFillColor(0);
	leg->AddEntry(oldCSVIVF_CvsDUSG,"oldCSVIVF","p");
	leg->AddEntry(CSVIVFV2_CvsDUSG,"CSVIVFV2","p");
//	leg->AddEntry(CSVIVFSL_CvsDUSG,"CSVIVFSL","p");
	leg->AddEntry(CSVLRctag_CvsDUSG,"CSVLRctag","p");
//	leg->AddEntry(CSVV2ctag_CvsDUSG,"CSVV2ctag","p");
	leg->AddEntry(CSVIVFSLctag_CvsDUSG,"CSVIVFSLctag","p");
	leg->Draw();

	//plotname = dir+"/FlavEffVsBEff_DUSG.png";
	//Plots1->Print(plotname.c_str());

	TCanvas * Plots2 = new TCanvas("Plots2","");
	Plots2->SetLogy();
	Plots2->SetGridx();
	Plots2->SetGridy();
	oldCSVIVF_CvsB = new TGraphErrors(n,oldCSVIVF_C,oldCSVIVF_B,oldCSVIVF_eC,oldCSVIVF_eB);
	oldCSVIVF_CvsB->GetXaxis()->SetTitle("C efficiency");
	//oldCSVIVF_CvsB->GetXaxis()->SetTitleOffset(1.2);
	oldCSVIVF_CvsB->GetXaxis()->SetRangeUser(0,1);
	oldCSVIVF_CvsB->GetYaxis()->SetTitle("B efficiency");
	oldCSVIVF_CvsB->GetYaxis()->SetTitleOffset(1.2);
	oldCSVIVF_CvsB->GetYaxis()->SetRangeUser(0.1,1);
	oldCSVIVF_CvsB->SetTitle("");
	oldCSVIVF_CvsB->SetMarkerColor(1);
	oldCSVIVF_CvsB->SetMarkerStyle(25);
	oldCSVIVF_CvsB->Draw("AP");	

	CSVIVFV2_CvsB = new TGraphErrors(n,CSVIVFV2_C,CSVIVFV2_B,CSVIVFV2_eC,CSVIVFV2_eB);
	CSVIVFV2_CvsB->SetMarkerColor(2);
	CSVIVFV2_CvsB->SetMarkerStyle(24);
	CSVIVFV2_CvsB->Draw("Psame");	

	CSVIVFSL_CvsB = new TGraphErrors(n,CSVIVFSL_C,CSVIVFSL_B,CSVIVFSL_eC,CSVIVFSL_eB);
	CSVIVFSL_CvsB->SetMarkerColor(9);
	CSVIVFSL_CvsB->SetMarkerStyle(29);
//	CSVIVFSL_CvsB->Draw("Psame");	

	CSVLRctag_CvsB = new TGraphErrors(n,CSVLRctag_C,CSVLRctag_B,CSVLRctag_eC,CSVLRctag_eB);
	CSVLRctag_CvsB->SetMarkerColor(6);
	CSVLRctag_CvsB->SetMarkerStyle(27);
	CSVLRctag_CvsB->Draw("Psame");	

	CSVV2ctag_CvsB = new TGraphErrors(n,CSVV2ctag_C,CSVV2ctag_B,CSVV2ctag_eC,CSVV2ctag_eB);
	CSVV2ctag_CvsB->SetMarkerColor(8);
	CSVV2ctag_CvsB->SetMarkerStyle(28);
//	CSVV2ctag_CvsB->Draw("Psame");	

	CSVIVFSLctag_CvsB = new TGraphErrors(n,CSVIVFSLctag_C,CSVIVFSLctag_B,CSVIVFSLctag_eC,CSVIVFSLctag_eB);
	CSVIVFSLctag_CvsB->SetMarkerColor(4);
	CSVIVFSLctag_CvsB->SetMarkerStyle(26);
	CSVIVFSLctag_CvsB->Draw("Psame");	

	leg = new TLegend(0.5,0.2,0.9,0.6);
	leg->SetFillColor(0);
	leg->AddEntry(oldCSVIVF_CvsB,"oldCSVIVF","p");
	leg->AddEntry(CSVIVFV2_CvsB,"CSVIVFV2","p");
//	leg->AddEntry(CSVIVFSL_CvsB,"CSVIVFSL","p");
	leg->AddEntry(CSVLRctag_CvsB,"CSVLRctag","p");
//	leg->AddEntry(CSVV2ctag_CvsB,"CSVV2ctag","p");
	leg->AddEntry(CSVIVFSLctag_CvsB,"CSVIVFSLctag","p");
	leg->Draw();

}
