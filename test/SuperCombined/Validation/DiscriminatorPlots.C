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
#include "/user/pvmulder/scripts/tdrstyle.C"

TFile *file1, *file2;
TLegend *leg;
string plotname;

void DiscriminatorPlots()
{
  using namespace std;

  setTDRStyle();
  gStyle->SetOptFit(0);
  gStyle->SetOptStat(0);


	string dir = "Plots";

	gSystem->mkdir(dir.c_str());

	TString fileName1 = "DQM_V0001_R000000001__POG__BTAG__SC_CSVSL.root";
	TString fileName2 = "../../CSVSL/Validation/DQM_V0001_R000000001__POG__BTAG__myCSVSL.root";
	file1 = TFile::Open(fileName1);
	file2 = TFile::Open(fileName2);

	if (!file1 || !file2) abort();

	TH1F * SCb = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/SC_GLOBAL/discr_SC_GLOBALB");
	TH1F * SCc = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/SC_GLOBAL/discr_SC_GLOBALC");
	TH1F * SCl = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/SC_GLOBAL/discr_SC_GLOBALDUS");
	TH1F * SCg = (TH1F*) file1->Get("DQMData/Run 1/Btag/Run summary/SC_GLOBAL/discr_SC_GLOBALG");

	SCb->SetTitle("");
	SCb->GetXaxis()->SetTitle("SC CSVSL");
  SCb->GetYaxis()->SetTitle("");
  SCb->GetYaxis()->SetTitleOffset(1.2);
//  SCb->SetMaximum(1000);
	SCb->GetXaxis()->SetRangeUser(-10,35);
	TCanvas * Plots = new TCanvas("Plots","");
  SCb->SetLineColor(2);
  SCc->SetLineColor(8);
  SCl->SetLineColor(4);
  SCg->SetLineColor(38);
  SCb->SetLineWidth(2);
  SCc->SetLineWidth(2);
  SCl->SetLineWidth(2);
  SCg->SetLineWidth(2);
  SCb->Draw();
  SCc->Draw("same");
  SCl->Draw("same");
  SCg->Draw("same");
	leg = new TLegend(0.2,0.6,0.5,0.9);
  leg->SetFillColor(0);
  leg->AddEntry(SCb,"b jets","l");
  leg->AddEntry(SCc,"c jets","l");
  leg->AddEntry(SCl,"l jets","l");
  leg->AddEntry(SCg,"g jets","l");
  leg->Draw();
	plotname = dir+"/SC_discriminator.png";
	Plots->Print(plotname.c_str());
	
	TH1F * CSVSLb = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALB");
	TH1F * CSVSLc = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALC");
	TH1F * CSVSLl = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALDUS");
	TH1F * CSVSLg = (TH1F*) file2->Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/discr_CSVSL_GLOBALG");

	CSVSLb->SetTitle("");
	CSVSLb->GetXaxis()->SetTitle("my CSVSL");
  CSVSLb->GetYaxis()->SetTitle("");
  CSVSLb->GetYaxis()->SetTitleOffset(1.2);
//  CSVSLb->SetMaximum(1000);
	CSVSLb->GetXaxis()->SetRangeUser(-10,35);
	TCanvas * Plots2 = new TCanvas("Plots2","");
  CSVSLb->SetLineColor(2);
  CSVSLc->SetLineColor(8);
  CSVSLl->SetLineColor(4);
  CSVSLg->SetLineColor(38);
  CSVSLb->SetLineWidth(2);
  CSVSLc->SetLineWidth(2);
  CSVSLl->SetLineWidth(2);
  CSVSLg->SetLineWidth(2);
  CSVSLb->Draw();
  CSVSLc->Draw("same");
  CSVSLl->Draw("same");
  CSVSLg->Draw("same");
	leg = new TLegend(0.2,0.6,0.5,0.9);
  leg->SetFillColor(0);
  leg->AddEntry(CSVSLb,"b jets","l");
  leg->AddEntry(CSVSLc,"c jets","l");
  leg->AddEntry(CSVSLl,"l jets","l");
  leg->AddEntry(CSVSLg,"g jets","l");
  leg->Draw();
	plotname = dir+"/myCSVSL_discriminator.png";
	Plots2->Print(plotname.c_str());
	
	
	}
