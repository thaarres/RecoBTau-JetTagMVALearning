######################################################################
###                                                                ###
### Script for plotting comparisons of different performances      ###
###                                                                ###
### Main thing to be changed by YOU: list of paths.                ###
###                                                                ###
### Easily adjustable                                              ###
### - legend                                                       ###
### - color                                                        ### 
###                                                                ###
### Assumes you have your CSV performance files                    ###
### in different directories for different training settings       ###
###                                                                ###
### TODO: - make it usable for pT/eta comparisons too              ###
###       - let setting be specified 'outside' the script when running
###                                                                ###
######################################################################
###                                                                ###
### What the user needs to do:                                     ###
###                                                                ###
### 1) Adjust the list of training settings that you would like to compare
### 2) Update the maps of paths/colors/legends such that the maps are not empty for you new variable
### 3) Run as python -i compareTrainings.py                    ###
###                                                                ###
######################################################################

from ROOT import *
gROOT.SetStyle("Plain")

############################################################################################ 
### This is the list of training settings you would like to compare                      ###
### => Change it if you would like to compare more/different settings.                   ###
### => If you add new variables, update the maps of path/color/legend accordingly (once) ###
############################################################################################ 

settingList = [
								"New (CMSSW_534, CSV LR)", #the CSVV1
#								"New (CMSSW_534, CSV git)", #the CSVV1 but in CMSSW_5_3_13_patch3 with git recipe 
#								"New (CMSSW_5313, CSV MLP)", #the CSV MLP with 7 more variables
 								"New (CMSSW_5314, CSV MLP newEnv)", # the CSV MLP with 7 more variables, but in environment with new GED variables etc. 
 								"New (CMSSW_5314, my CSVSL)" # the CSVSL combining the input variables of CSV MLP newEnv and SL  
               ]

#################################################
### here are just some maps of paths          ###
###  and legend names and colors for plotting ###
### - paths: adjust only once                 ### 
### - legend/color: adjust when you want      ###
#################################################

path = "/user/gvonsem/BTagServiceWork/MVA/testBtagVal_NewJuly2012/CMSSW_5_3_4_patch1/src/Validation/RecoB/"

pathList = {
						"New (CMSSW_534, CSV LR)": "/user/gvonsem/BTagServiceWork/MVA/testBtagVal_NewJuly2012/CMSSW_5_3_4_patch1/src/Validation/RecoB/test_withPFnoPU/INTERACTIVE_validationwithPFnoPU_Fix_Adding2HighPtBins_nonFit-Reweighting/DQM_V0001_R000000001__POG__BTAG__categories.root",
						"New (CMSSW_534, CSV git)": "/user/kderoove/bTagging/CMSSW_5_3_13_patch3/src/Validation/RecoB/test/CSV_LR_gitRecipeTest/DQM_V0001_R000000001__POG__BTAG__BJET.root",
						"New (CMSSW_5313, CSV MLP)": "/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/GIT_Recipe/CMSSW_5_3_14/src/RecoBTau/JetTagMVALearning/test/CSV_MLP/Validation/DQM_V0001_R000000001__POG__BTAG__CSVMLP_oldenv.root",
						"New (CMSSW_5314, CSV MLP newEnv)": "/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/GIT_Recipe/CMSSW_5_3_14/src/RecoBTau/JetTagMVALearning/test/CSV_MLP/Validation/DQM_V0001_R000000001__POG__BTAG__CSVMLP_CSVV2dev.root",
						"New (CMSSW_5314, my CSVSL)": "/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/SuperTaggerDev/CMSSW_5_3_14/src/RecoBTau/JetTagMVALearning/test/CSVSL/Validation/DQM_V0001_R000000001__POG__BTAG__myCSVSL.root"
}

leg = {
				"New (CMSSW_534, CSV LR)": "CSVV1",
				"New (CMSSW_534, CSV git)": "CSVV1 git",
				"New (CMSSW_5313, CSV MLP)": "CSVV2 7 vars",
				"New (CMSSW_5314, CSV MLP newEnv)": "CSVV2",
				"New (CMSSW_5314, my CSVSL)": "my CSVSL"
       }

color = {
			"New (CMSSW_534, CSV LR)": 1,
			"New (CMSSW_534, CSV git)": 8,
			"New (CMSSW_5313, CSV MLP)": 2,
			"New (CMSSW_5314, CSV MLP newEnv)": 4,
			"New (CMSSW_5314, my CSVSL)": 2#,
         }

#####################################
### Now we're gonna loop and plot ###
#####################################
   
plotList1bin   = {}
plotList1bin_C = {}
plotList   = {}
plotList_C = {}

for setting in settingList:
    ### Get file and plot
    fileName = pathList[setting]
    file     = TFile.Open(fileName)
    print setting
    if setting == "New (CMSSW_534, CSV LR)"   or setting == "New (CMSSW_534, CSV git)" or setting == "New (CMSSW_5313, CSV MLP)" or setting == "New (CMSSW_5314, CSV MLP newEnv)":
       plot1bin     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_0-1v2_PT_90-150/FlavEffVsBEff_DUSG_discr_CSV_ETA_0-1v2_PT_90-150")
       plot1bin_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_ETA_0-1v2_PT_90-150/FlavEffVsBEff_C_discr_CSV_ETA_0-1v2_PT_90-150")
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/FlavEffVsBEff_DUSG_discr_CSV_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSV_GLOBAL/FlavEffVsBEff_C_discr_CSV_GLOBAL")
    elif setting == "New (CMSSW_5314, my CSVSL)":
       plot1bin     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_0-1v2_PT_90-150/FlavEffVsBEff_DUSG_discr_CSVSL_ETA_0-1v2_PT_90-150")
       plot1bin_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_ETA_0-1v2_PT_90-150/FlavEffVsBEff_C_discr_CSVSL_ETA_0-1v2_PT_90-150")
       plot     = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/FlavEffVsBEff_DUSG_discr_CSVSL_GLOBAL")
       plot_C   = file.Get("DQMData/Run 1/Btag/Run summary/CSVSL_GLOBAL/FlavEffVsBEff_C_discr_CSVSL_GLOBAL")
    else :
       print "check path to DQM file or histogram directory and name inside the DQM file"
		### Set name of plot
    plot1bin.SetName(pathList[setting])
    plot1bin_C.SetName(pathList[setting])
    plot.SetName(pathList[setting])
    plot_C.SetName(pathList[setting])
    ### Fill plot list
    plotList1bin[setting]   = plot1bin  
    plotList1bin_C[setting] = plot1bin_C
    plotList[setting]   = plot  
    plotList_C[setting] = plot_C


### Make canvas ###

Plots2 = TCanvas("Plots2","",1200,600)
Plots2.Divide(2)

Plots2.cd(1).SetLogy()
Plots2.cd(1).SetGrid()

leg3 = TLegend(0.15,0.6,0.5,0.9)
leg3.SetFillColor(0);

### and draw ###

first=true
for setting in settingList:
    plotList[setting].SetMarkerColor(color[setting])
    plotList[setting].SetMarkerStyle(25)
    if first:
        plotList[setting].GetXaxis().SetTitle("B efficiency")
        plotList[setting].GetYaxis().SetTitle("DUSG efficiency")
        plotList[setting].GetXaxis().SetRangeUser(0.3,1.0)
        plotList[setting].GetYaxis().SetRangeUser(0.0001,1.0)
        plotList[setting].SetTitle("")
        plotList[setting].Draw()
        first=false
    else         :
        plotList[setting].Draw("same")  
    leg3.AddEntry(plotList[setting],leg[setting],"p")
  
leg3.Draw()

###################
### Second plot ###
###################

Plots2.cd(2).SetLogy()
Plots2.cd(2).SetGrid()

## and draw again

first=true
for setting in settingList:
    plotList_C[setting].SetMarkerColor(color[setting])
    plotList_C[setting].SetMarkerStyle(25)
    if first:
        plotList_C[setting].Draw()
        plotList_C[setting].GetXaxis().SetTitle("B efficiency")
        plotList_C[setting].GetYaxis().SetTitle("C efficiency")
        plotList_C[setting].GetXaxis().SetRangeUser(0.2,1.0)
        plotList_C[setting].GetYaxis().SetRangeUser(0.001,1.0)
        plotList_C[setting].SetTitle("")
        first=false
    else         :
        plotList_C[setting].Draw("same")  

###########
### FIN ###
###########
