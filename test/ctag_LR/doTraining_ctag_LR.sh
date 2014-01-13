echo "BEFORE RUNNING THIS OUT OF THE BOX, CHECK THE INSTRUCTIONS"
echo "https://twiki.cern.ch/twiki/bin/view/CMS/BTagSoftwareMVATrainer"

#read -p "PARALLEL PROCESSING: how many cores can you afford? " answer

answer=6

#echo "start the training, make sure you extracted the variables first using cmsRun VariableExtractor_LR_cfg.py (usually QCD events are used)"
#
##!/bin/sh
# ===== NO IVF files
#path_to_rootfiles=/gpfs/cms/users/umer/CMSSW_5_3_7_patch4/src/work/testBtagVal/RootFiles_LR_withPFnoPU_withhighpt
#path_to_bias=/gpfs/cms/users/umer/CMSSW_5_3_7_patch4/src/work/testBtagVal/RootFiles_LR_TTbar_forbias

# ===== IVF files
# path_to_rootfiles=/gpfs/cms/users/umer/CMSSW_5_3_7_patch4/src/work/testBtagVal/RootFiles_QCDhighpT_53X_PFnoPU_highPT_IVF_TagInfosNotFiltered
# path_to_bias=/gpfs/cms/users/umer/CMSSW_5_3_7_patch4/src/work/testBtagVal/Trees_TTJetsInclusive_IVF_forbias

# ===== IVF with NI removal files
# path_to_rootfiles=/gpfs/cms/users/umer/CMSSW_5_3_13_patch3/src/work/TrainingTrees/TrainingTrees_IVF_nVtxTot_NIrejection_QCD/
# path_to_bias=/gpfs/cms/users/umer/CMSSW_5_3_13_patch3/src/work/TrainingTrees/Trees_IVF_nVtxTot_NIrejection_TTJets/

# ===== my prouction, IVF with NI removal + NO cut on min decay len
# path_to_rootfiles=/gpfs/cms/users/umer/work/cTag/test_validation/TTbar_IVF_NOmindecaylen
# path_to_bias=/gpfs/cms/users/umer/work/cTag/test_validation/QCD_IVF_NOmindecaylen

# ===== NO IVF files, with added variables
path_to_rootfiles=/gpfs/cms/users/umer/CMSSW_5_3_14/src/work/RootFiles_cTag_NewVars/QCD
path_to_bias=/gpfs/cms/users/umer/CMSSW_5_3_14/src/work/RootFiles_cTag_NewVars/TTbar_bias

prefix=CombinedSV
Combinations="NoVertex_C_DUSG NoVertex_C_B PseudoVertex_C_DUSG PseudoVertex_C_B RecoVertex_C_DUSG RecoVertex_C_B"

CAT="Reco Pseudo No"

#echo "Merging the rootfiles" 

#for i in $CAT ; do

#	hadd $path_to_rootfiles/${prefix}${i}Vertex_C_DUSG.root $path_to_rootfiles/${prefix}${i}Vertex_DUSG.root $path_to_rootfiles/${prefix}${i}Vertex_C.root
#	hadd $path_to_rootfiles/${prefix}${i}Vertex_C_B.root $path_to_rootfiles/${prefix}${i}Vertex_B.root $path_to_rootfiles/${prefix}${i}Vertex_C.root
#done


echo "Filling the 2D pt/eta histograms" 

g++ ../ctag_templatefiles/histoJetEtaPt.cpp `root-config --cflags --glibs` -o histos
./histos $path_to_rootfiles $prefix


# NOTE to self: this part has to remain
echo "Calculating the pt/eta weights"

for j in $( ls ../ctag_templatefiles/MVATrainer_*cfg.py ) ; do cp $j . ; done
for j in $( ls MVATrainer_*cfg.py ) ; do
     cat $j | grep '"./'$prefix''
     if [ $? -eq 0  ]; then
         sed -i 's@"./'$prefix'@"'$path_to_rootfiles'/'$prefix'@g#' $j # change the path of the input rootfiles                                     
     else
         echo " WARNING no matches were found in " $j
     fi 
done

for j in $( ls ../ctag_templatefiles/Save_*xml ) ; do cp $j . ; done
# this is unnecessary because it changes the CombinedSV to CombinedSV
# for j in $( ls Save*xml ) ; do
# 	sed -i 's@CombinedSV@'$prefix'@g#' $j # change the name of the tag in the file
# done


echo "Reweighting the trees according to the pt/eta weights and saving the relevant variables " 

files=("MVATrainer_No_C_DUSG_cfg.py" "MVATrainer_No_C_B_cfg.py" "MVATrainer_Pseudo_C_DUSG_cfg.py" "MVATrainer_Pseudo_C_B_cfg.py" "MVATrainer_Reco_C_DUSG_cfg.py" "MVATrainer_Reco_C_B_cfg.py")
l=0
while [ $l -lt 6 ]
do
	jobsrunning=0
	while [ $jobsrunning -lt $answer ]
	do
		nohup cmsRun ${files[l]} &
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done

echo "Calculating the bias: ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"
g++ ../ctag_templatefiles/biasForXml.cpp `root-config --cflags --glibs` -o bias
./bias $path_to_bias $prefix
echo "ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"

echo "Replacing the bias tables in the Train*xml files "
for i in $Combinations ; do
 	sed -n -i '/<bias_table>/{p; :a; N; /<\/bias_table>/!ba; s/.*\n//}; p' Train_${i}.xml # remove bias table in file
 	for line in $( cat ${i}.txt ) ; do 
 		echo "$line" 
 		newline2=$(cat Train_${i}.xml | grep -n '</bias_table>' | grep -o '^[0-9]*')
 		sed -i ${newline2}'i\'$line Train_${i}.xml
 	done 
done

Vertex="NoVertex PseudoVertex RecoVertex"
Flavour="C_DUSG C_B"
for k in $Vertex ; do
 	for l in $Flavour ; do
 		sed -n -i '/<bias_table><!--'$l'-->/{p; :a; N; /<\/bias_table><!--'$l'-->/!ba; s/.*\n//}; p' Train_${k}.xml #remove bias table in file
  		for line in $( cat ${k}_${l}.txt ) ; do 
  			echo "$line" 
 			newline1=$(cat Train_${k}.xml | grep -n '</bias_table><!--'$l'-->' | grep -o '^[0-9]*')
 			sed -i ${newline1}'i\'$line Train_${k}.xml
 		done
 	done
done

echo end of bias calculation

echo "Do the actual training"

CombinationsArray=("NoVertex_C_DUSG" "NoVertex_C_B" "PseudoVertex_C_DUSG" "PseudoVertex_C_B" "RecoVertex_C_DUSG" "RecoVertex_C_B")
l=0
while [ $l -lt 6 ]
do
	jobsrunning=0
	while [[ $jobsrunning -lt $answer && $jobsrunning -lt 6 ]] 
	do
		echo Processing ${CombinationsArray[l]}
 		mkdir tmp${CombinationsArray[l]}
 		cd tmp${CombinationsArray[l]}
		echo Train_${CombinationsArray[l]}.xml
		echo train_${CombinationsArray[l]}_save.root
		nohup mvaTreeTrainer ../Train_${CombinationsArray[l]}.xml tmp.mva ../train_${CombinationsArray[l]}_save.root &
		cd ..
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done
 
echo "Combine the C versus DUSG and C versus B training "

VertexCategory=("NoVertex" "PseudoVertex" "RecoVertex")
l=0
while [ $l -lt 3 ]
do
	jobsrunning=0
	while [[ $jobsrunning -lt $answer  && $jobsrunning -lt 3 ]] 
	do
	  echo tmp${VertexCategory[l]}_C_*/*.xml
		cp tmp${VertexCategory[l]}_C_*/*.xml .
 		nohup mvaTreeTrainer -l Train_${VertexCategory[l]}.xml ${prefix}${VertexCategory[l]}.mva train_${VertexCategory[l]}_C_DUSG_save.root train_${VertexCategory[l]}_C_B_save.root &
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done


echo "do now manually cmsRun ../copyMVAToSQLite_cfg.py to copy the mva training output to sqlite format"
#echo "run the validation from Validation/RecoB/test/ afterwards -> usually on ttbar events, make sure you read in the *db file produced in the previous step"
# echo "----> an example of how to do it can be found in UserCode/PetraVanMulders/BTagging/CSVLR_default/reco_validationNEW_CSVMVA_categories_cfg.py"

# nohup cmsRun ../copyMVAToSQLite_cfg.py
# nohup cmsRun reco_validation_CSVMVA_cfg.py
