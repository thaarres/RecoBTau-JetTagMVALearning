echo "BEFORE RUNNING THIS OUT OF THE BOX, CHECK THE INSTRUCTIONS"
echo "https://twiki.cern.ch/twiki/bin/view/CMS/BTagSoftwareMVATrainer"

#read -p "PARALLEL PROCESSING: how many cores can you afford? " answer

echo "ADAPT BIASES IF NECESSARY!!!"

#echo "Calculating the bias: ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"
#g++ biasForXml.cpp `root-config --cflags --glibs` -o bias
#./bias $path_to_rootfiles $prefix
#echo "ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"

answer=6

path_to_rootfiles=/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/SuperTaggerDev/CMSSW_5_3_14/src/RootFiles/SkimmedRootFiles/
#Combinations=("NoVertexNoSoftLepton_B_DUSG" "NoVertexNoSoftLepton_B_C" "PseudoVertexNoSoftLepton_B_DUSG" "PseudoVertexNoSoftLepton_B_C" "RecoVertexNoSoftLepton_B_DUSG" "RecoVertexNoSoftLepton_B_C" "NoVertexSoftElectron_B_DUSG" "NoVertexSoftElectron_B_C" "PseudoVertexSoftElectron_B_DUSG" "PseudoVertexSoftElectron_B_C" "RecoVertexSoftElectron_B_DUSG" "RecoVertexSoftElectron_B_C" "NoVertexSoftMuon_B_DUSG" "NoVertexSoftMuon_B_C" "PseudoVertexSoftMuon_B_DUSG" "PseudoVertexSoftMuon_B_C" "RecoVertexSoftMuon_B_DUSG" "RecoVertexSoftMuon_B_C")
Combinations=("NoVertexNoSoftLepton_B_DUSG" "NoVertexNoSoftLepton_B_C" "PseudoVertexNoSoftLepton_B_DUSG" "PseudoVertexNoSoftLepton_B_C" "RecoVertexNoSoftLepton_B_DUSG" "RecoVertexNoSoftLepton_B_C")
prefix="CombinedSV"

echo "Filling the 2D pt/eta histograms" 

#g++ ./histoJetEtaPt.cpp `root-config --cflags --glibs` -o histos
#./histos $path_to_rootfiles $prefix
#
#echo "Reweighting the trees according to the pt/eta weights and saving the relevant variables " 
#
#l=0
#while [ $l -lt 18 ]
#do
#	jobsrunning=0
#	while [[ $jobsrunning -lt $answer && $l -lt 18 ]] # for some reason stuck after the first 6 jobs???
#	do
#		echo MVATrainer_${Combinations[l]}_cfg.py
#		nohup cmsRun MVATrainer_${Combinations[l]}_cfg.py &
#		let jobsrunning=$jobsrunning+1
#		let l=$l+1
#	done
#	wait
#done
#
#
echo "Do the actual training"

l=0
#while [ $l -lt 18 ]
while [ $l -lt 6 ]
do
	jobsrunning=0
#	while [[ $jobsrunning -lt $answer && $jobsrunning -lt 18 ]] 
	while [[ $jobsrunning -lt $answer && $jobsrunning -lt 6 ]] 
	do
		echo Processing ${Combinations[l]}
 		mkdir tmp${Combinations[l]}
 		cd tmp${Combinations[l]}
		echo mvaTreeTrainer ../Train_${Combinations[l]}.xml tmp.mva ../train_${Combinations[l]}_save.root
		nohup mvaTreeTrainer ../Train_${Combinations[l]}.xml tmp.mva ../train_${Combinations[l]}_save.root &
		cd ..
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done


echo "Combine the B versus DUSG and B versus C training "

#VertexCategory=("NoVertexNoSoftLepton" "PseudoVertexNoSoftLepton" "RecoVertexNoSoftLepton" "NoVertexSoftElectron" "PseudoVertexSoftElectron" "RecoVertexSoftElectron" "NoVertexSoftMuon" "PseudoVertexSoftMuon" "RecoVertexSoftMuon")
VertexCategory=("NoVertexNoSoftLepton" "PseudoVertexNoSoftLepton" "RecoVertexNoSoftLepton")
l=0
#while [ $l -lt 9 ]
while [ $l -lt 3 ]
do
	jobsrunning=0
	while [[ $jobsrunning -lt $answer  && $jobsrunning -lt 3 ]] 
	do
 		mkdir tmp${VertexCategory[l]}
 		cd tmp${VertexCategory[l]}
		cp ../tmp${VertexCategory[l]}_B_C/*.xml .
		cp ../tmp${VertexCategory[l]}_B_C/*.txt .
		cp ../tmp${VertexCategory[l]}_B_DUSG/*.xml .
		cp ../tmp${VertexCategory[l]}_B_DUSG/*.txt .
		echo mvaTreeTrainer -l ../Train_${VertexCategory[l]}.xml ${prefix}MVA_${VertexCategory[l]}.mva ../train_${VertexCategory[l]}_B_DUSG_save.root ../train_${VertexCategory[l]}_B_C_save.root
 		nohup mvaTreeTrainer -l ../Train_${VertexCategory[l]}.xml ${prefix}MVA_${VertexCategory[l]}.mva ../train_${VertexCategory[l]}_B_DUSG_save.root ../train_${VertexCategory[l]}_B_C_save.root &
		cd ..
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done

