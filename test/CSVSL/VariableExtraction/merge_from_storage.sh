#!/bin/bashJetFlavourPUid/CSVSLIVF

maindirec=/pnfs/iihe/cms/store/user/`whoami`/BtagExtractor_5314_JetFlavourPUid/CSVSLIVF/

#dirs_to_merge=( TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM )
#dirs_to_merge=( TTJets_SemiLeptMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A_ext-v1_AODSIM )
#dirs_to_merge=( TTJets_FullLeptMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM )
#dirs_to_merge=( TTJets_HadronicMGDecays_8TeV-madgraph_Summer12_DR53X-PU_S10_START53_V7A_ext-v1_AODSIM )

dirs_to_merge=( QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM QCD_Pt-1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM )

homedirec=/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/

CAT=(CombinedSVRecoVertexNoSoftLepton CombinedSVPseudoVertexNoSoftLepton CombinedSVNoVertexNoSoftLepton CombinedSVRecoVertexSoftElectron CombinedSVPseudoVertexSoftElectron CombinedSVNoVertexSoftElectron CombinedSVRecoVertexSoftMuon CombinedSVPseudoVertexSoftMuon CombinedSVNoVertexSoftMuon )

#FLAV=(B C DUSG)
FLAV=(D U S G)

mkdir $homedirec/QCD_training
cd $homedirec/QCD_training

for l in ${dirs_to_merge[@]} ;
do
	for k in ${CAT[@]} ;
	do
		for j in $( ls $maindirec/$l/${k}_B*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Bfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_C*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Cfiles.txt; done
		if [ $k=="CombinedSVNoVertexNoSoftLepton" ]
		then
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_D*); do
				echo "at file number $countfiles" 
				((countfiles++))
#				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}Dfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_U*); do 
				echo "at file number $countfiles" 
				((countfiles++))
#				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}Ufiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_S*); do 
				echo "at file number $countfiles" 
				((countfiles++))
#				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}Sfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_G*); do 
				echo "at file number $countfiles" 
				((countfiles++))
#				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 20 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "dcap://maite.iihe.ac.be/$j " >> ${k}Gfiles.txt
			done
		else
			for j in $( ls $maindirec/$l/${k}_D*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Dfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_U*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Ufiles.txt; done
			for j in $( ls $maindirec/$l/${k}_S*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Sfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_G*); do printf "dcap://maite.iihe.ac.be/$j " >> ${k}Gfiles.txt; done			
		fi
	done
done	

for k in ${CAT[@]} ;
do
	for i in ${FLAV[@]} ;
	do
#		echo cat ${k}${i}files.txt
		rootfiles=`cat ${k}${i}files.txt`
		hadd tmp.root $rootfiles
		mv tmp.root ${k}_${i}.root
	done
done

