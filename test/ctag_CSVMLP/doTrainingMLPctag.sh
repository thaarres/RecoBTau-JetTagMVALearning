echo "BEFORE RUNNING THIS OUT OF THE BOX, CHECK THE INSTRUCTIONS"
echo "https://twiki.cern.ch/twiki/bin/view/CMS/BTagSoftwareMVATrainer"

#read -p "PARALLEL PROCESSING: how many cores can you afford? " answer

echo "ADAPT BIASES IF NECESSARY!!!"
echo ">>>> IF YOU DON'T KNOW WHAT IS MEANT: ASK SOMEONE ;-)"

answer=3

#echo "start the training, make sure you extracted the variables first using cmsRun VariableExtractor_LR_cfg.py (usually QCD events are used)"
#
##!/bin/sh
path_to_rootfiles=/afs/cern.ch/work/p/pvmulder/public/BTagging/RootFiles_QCDhighpT_53X/
prefix="CombinedSVV2"
Combinations="NoVertex_C_DUSG NoVertex_C_B PseudoVertex_C_DUSG PseudoVertex_C_B RecoVertex_C_DUSG RecoVertex_C_B"
CAT="Reco Pseudo No"


#echo "Merging the rootfiles" 

#for i in $CAT ; do
##	hadd $path_to_rootfiles/${prefix}${i}Vertex_DUSG.root $path_to_rootfiles/${prefix}${i}Vertex_D.root $path_to_rootfiles/${prefix}${i}Vertex_U.root $path_to_rootfiles/${prefix}${i}Vertex_S.root $path_to_rootfiles/${prefix}${i}Vertex_G.root 
#	hadd $path_to_rootfiles/${prefix}${i}Vertex_C_DUSG.root $path_to_rootfiles/${prefix}${i}Vertex_DUSG.root $path_to_rootfiles/${prefix}${i}Vertex_C.root
#	hadd $path_to_rootfiles/${prefix}${i}Vertex_C_B.root $path_to_rootfiles/${prefix}${i}Vertex_C.root $path_to_rootfiles/${prefix}${i}Vertex_B.root
#done


#echo "Filling the 2D pt/eta histograms" 

#g++ ../histoJetEtaPt.cpp `root-config --cflags --glibs` -o histos
#./histos $path_to_rootfiles $prefix

echo "Calculating the pt/eta weights"

for j in $( ls ../MVATrainer_*cfg.py ) ; do cp $j . ; done
for j in $( ls MVATrainer_*cfg.py ) ; do
#	sed -i 's@CombinedSV@'$prefix'@g#' $j # change the path of the input rootfiles
	sed -i 's@"./'$prefix'@"'$path_to_rootfiles'/'$prefix'@g#' $j # change the path of the input rootfiles
done

#for j in $( ls ../Save_*xml ) ; do cp $j . ; done
#for j in $( ls Save*xml ) ; do
#	sed -i 's@CombinedSV@'$prefix'@g#' $j # change the name of the tag in the file
#done


echo "Reweighting the trees according to the pt/eta weights and saving the relevant variables " 

files=("MVATrainer_No_C_DUSG_cfg.py" "MVATrainer_No_C_B_cfg.py" "MVATrainer_Pseudo_C_DUSG_cfg.py" "MVATrainer_Pseudo_C_B_cfg.py" "MVATrainer_Reco_C_DUSG_cfg.py" "MVATrainer_Reco_C_B_cfg.py")

l=0
while [ $l -lt 6 ]
do
	jobsrunning=0
	while [ $jobsrunning -lt $answer ]
	do
	  #echo ${files[l]}
		nohup cmsRun ${files[l]} &
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done

echo ">>>> CHECK THAT THE train*_save.root FILES ARE CORRECTLY PRODUCED! OPEN A FILE AND CHECK THAT THE WEIGHT BRANCH IS NOT EMPTY...."


#echo "Calculating the bias: ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"
#g++ biasForXml.cpp `root-config --cflags --glibs` -o bias
#./bias $path_to_rootfiles $prefix
#echo "ARE YOU SURE THAT YOU HAVE ENOUGH STATISTICS TO DETERMINE THE BIAS ACCURATELY?"
#
#echo "Replacing the bias tables in the Train*xml files "
#for i in $Combinations ; do
#	sed -n -i '/<bias_table>/{p; :a; N; /<\/bias_table>/!ba; s/.*\n//}; p' Train_${i}.xml # remove bias table in file
#	for line in $( cat ${i}.txt ) ; do 
#		echo "$line" 
#		newline2=$(cat Train_${i}.xml | grep -n '</bias_table>' | grep -o '^[0-9]*')
#		sed -i ${newline2}'i\'$line Train_${i}.xml
#	done 
#done
#
#Vertex="NoVertex PseudoVertex RecoVertex"
#Flavour="C_DUSG C_B"
#for k in $Vertex ; do
#	for l in $Flavour ; do
#		sed -n -i '/<bias_table><!--'$l'-->/{p; :a; N; /<\/bias_table><!--'$l'-->/!ba; s/.*\n//}; p' Train_${k}.xml # remove bias table in file
#		for line in $( cat ${k}_${l}.txt ) ; do 
#			echo "$line" 
#			newline1=$(cat Train_${k}.xml | grep -n '</bias_table><!--'$l'-->' | grep -o '^[0-9]*')
#			sed -i ${newline1}'i\'$line Train_${k}.xml
#		done
#	done
#done
#

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
		cp tmp${VertexCategory[l]}_B_*/*.xml .
 		nohup mvaTreeTrainer -l Train_${VertexCategory[l]}.xml ${prefix}${VertexCategory[l]}.mva train_${VertexCategory[l]}_C_DUSG_save.root train_${VertexCategory[l]}_C_B_save.root &
		let jobsrunning=$jobsrunning+1
		let l=$l+1
	done
	wait
done


echo "training DONE"
