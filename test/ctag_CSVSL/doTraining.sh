echo "BEFORE RUNNING THIS OUT OF THE BOX, CHECK THE INSTRUCTIONS"
echo "https://twiki.cern.ch/twiki/bin/view/CMS/BTagSoftwareMVATrainer"

#read -p "PARALLEL PROCESSING: how many cores can you afford? " answer


answer=6

path_to_rootfiles=/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/QCD_training/
path_to_biases=/gpfs/cms/users/umer/CMSSW_5_3_16/src/work/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/TTbar_biases/

Combinations=("NoVertexNoSoftLepton_C_DUSG" "NoVertexNoSoftLepton_C_B" "PseudoVertexNoSoftLepton_C_DUSG" "PseudoVertexNoSoftLepton_C_B" "RecoVertexNoSoftLepton_C_DUSG" "RecoVertexNoSoftLepton_C_B" "NoVertexSoftElectron_C_DUSG" "NoVertexSoftElectron_C_B" "PseudoVertexSoftElectron_C_DUSG" "PseudoVertexSoftElectron_C_B" "RecoVertexSoftElectron_C_DUSG" "RecoVertexSoftElectron_C_B" "NoVertexSoftMuon_C_DUSG" "NoVertexSoftMuon_C_B" "PseudoVertexSoftMuon_C_DUSG" "PseudoVertexSoftMuon_C_B" "RecoVertexSoftMuon_C_DUSG" "RecoVertexSoftMuon_C_B")
#Combinations=("NoVertexNoSoftLepton_C_DUSG" "NoVertexNoSoftLepton_C_B" "PseudoVertexNoSoftLepton_C_DUSG" "PseudoVertexNoSoftLepton_C_B" "RecoVertexNoSoftLepton_C_DUSG" "RecoVertexNoSoftLepton_C_B")
prefix="CombinedSV"

# NOTE: currently done by hand
# echo "Merging the rootfiles" 

CAT=("NoVertexNoSoftLepton" "PseudoVertexNoSoftLepton" "RecoVertexNoSoftLepton" "NoVertexSoftMuon" "PseudoVertexSoftMuon" "RecoVertexSoftMuon" "NoVertexSoftElectron" "PseudoVertexSoftElectron" "RecoVertexSoftElectron")

#for i in ${CAT[@]} ; do
#	hadd $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_C_DUSG.root $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_DUSG.root $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_C.root
#	hadd $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_C_B.root $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_B.root $path_to_rootfiles/skimmed_20k_eachptetabin_${prefix}${i}_C.root
#done


 # echo "ADAPT BIASES IF NECESSARY!!!"

 # echo "Calculating the bias: ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"
 # g++ biasForXml.cpp `root-config --cflags --glibs` -o bias
 # ./bias $path_to_biases $prefix
 # echo "ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"

#echo "Replacing the bias tables in the Train*xml files "
#for i in ${Combinations[@]} ; do
#        sed -n -i '/<bias_table>/{p; :a; N; /<\/bias_table>/!ba; s/.*\n//}; p' Train_${i}.xml # remove bias table in file                                                                                                       
#        for line in $( cat ${i}.txt ) ; do
#echo "$line"
#                newline2=$(cat Train_${i}.xml | grep -n '</bias_table>' | grep -o '^[0-9]*')
#                sed -i ${newline2}'i\'$line Train_${i}.xml
#        done
#done
#
#Flavour=("C_DUSG C_B")
#for k in ${CAT[@]} ; do
#        for l in ${Flavour[@]} ; do
#                sed -n -i '/<bias_table><!--'$l'-->/{p; :a; N; /<\/bias_table><!--'$l'-->/!ba; s/.*\n//}; p' Train_${k}.xml #remove bias table in file                                                                          
#                for line in $( cat ${k}_${l}.txt ) ; do
#echo "$line"
#                        newline1=$(cat Train_${k}.xml | grep -n '</bias_table><!--'$l'-->' | grep -o '^[0-9]*')
#                        sed -i ${newline1}'i\'$line Train_${k}.xml
#                done
#        done
#done
#
#echo end of bias calculation
#


#echo "Filling the 2D pt/eta histograms" 
#
#g++ ./histoJetEtaPt.cpp `root-config --cflags --glibs` -o histos
#./histos $path_to_rootfiles $prefix

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


#echo "Do the actual training"
#
#l=0
#while [ $l -lt 18 ]
##while [ $l -lt 6 ]
#do
#	jobsrunning=0
#	while [[ $jobsrunning -lt $answer && $jobsrunning -lt 18 ]] 
##	while [[ $jobsrunning -lt $answer && $jobsrunning -lt 6 ]] 
#	do
#		echo Processing ${Combinations[l]}
# 		mkdir tmp${Combinations[l]}
# 		cd tmp${Combinations[l]}
#		echo mvaTreeTrainer ../Train_${Combinations[l]}.xml tmp.mva ../train_${Combinations[l]}_save.root
#		nohup mvaTreeTrainer ../Train_${Combinations[l]}.xml tmp.mva ../train_${Combinations[l]}_save.root &
#		cd ..
#		let jobsrunning=$jobsrunning+1
#		let l=$l+1
#	done
#	wait
#done
#

 echo "Combine the C versus DUSG and C versus B training "

 VertexCategory=("NoVertexNoSoftLepton" "PseudoVertexNoSoftLepton" "RecoVertexNoSoftLepton" "NoVertexSoftElectron" "PseudoVertexSoftElectron" "RecoVertexSoftElectron" "NoVertexSoftMuon" "PseudoVertexSoftMuon" "RecoVertexSoftMuon")
 #VertexCategory=("NoVertexNoSoftLepton" "PseudoVertexNoSoftLepton" "RecoVertexNoSoftLepton")
 l=0
 while [ $l -lt 9 ]
 #while [ $l -lt 3 ]
 do
 	jobsrunning=0
 	while [[ $jobsrunning -lt $answer  && $jobsrunning -lt 9 ]] 
 	do
  		mkdir tmp${VertexCategory[l]}
  		cd tmp${VertexCategory[l]}
 		cp ../tmp${VertexCategory[l]}_C_B/*.xml .
 		cp ../tmp${VertexCategory[l]}_C_B/*.txt .
 		cp ../tmp${VertexCategory[l]}_C_DUSG/*.xml .
 		cp ../tmp${VertexCategory[l]}_C_DUSG/*.txt .
 		echo mvaTreeTrainer -l ../Train_${VertexCategory[l]}.xml ${prefix}MVA_${VertexCategory[l]}.mva ../train_${VertexCategory[l]}_C_DUSG_save.root ../train_${VertexCategory[l]}_C_B_save.root
  		nohup mvaTreeTrainer -l ../Train_${VertexCategory[l]}.xml ${prefix}MVA_${VertexCategory[l]}.mva ../train_${VertexCategory[l]}_C_DUSG_save.root ../train_${VertexCategory[l]}_C_B_save.root &
 		cd ..
 		let jobsrunning=$jobsrunning+1
 		let l=$l+1
 	done
 	wait
 done

echo "TRAINING DONE"
