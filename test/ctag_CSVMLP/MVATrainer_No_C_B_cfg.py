import FWCore.ParameterSet.Config as cms

process = cms.Process("IPTrainer")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.CombinedSVV2Trainer = cms.EDAnalyzer("JetTagMVATreeTrainer",
	useCategories		= cms.bool(False),
	calibrationRecord	= cms.string("CombinedSVV2NoVertex"),
	ignoreFlavours		= cms.vint32(0, 1, 2, 3, 21),
	signalFlavours		= cms.vint32(4),
	minimumTransverseMomentum = cms.double(15.0),
	minimumPseudoRapidity	= cms.double(0),
	maximumPseudoRapidity	= cms.double(2.5),

	factor = cms.double(1),
	bound = cms.double(50),

	fileNames = cms.vstring(
		" /afs/cern.ch/work/p/pvmulder/public/BTagging/GIT_SETUP/TEST_RECIPE/CMSSW_5_3_13_patch3/src/RootFiles_CMSSW5313_gitrecipe/QCD/skimmed_20k_eachptetabin_CombinedSVV2NoVertex_C.root",
		" /afs/cern.ch/work/p/pvmulder/public/BTagging/GIT_SETUP/TEST_RECIPE/CMSSW_5_3_13_patch3/src/RootFiles_CMSSW5313_gitrecipe/QCD/skimmed_20k_eachptetabin_CombinedSVV2NoVertex_B.root"
	),
	weightFile = cms.string("weights/CombinedSVV2NoVertex_CB_histo.txt"),
	biasFiles = cms.vstring(
		"-",
		"*",
		"weights/CombinedSVV2NoVertex_C_B_ratio.txt"
	)
)

process.looper = cms.Looper("JetTagMVATrainerLooper",
	trainers = cms.VPSet(
		cms.PSet(
			calibrationRecord = cms.string("CombinedSVV2NoVertex"),
			trainDescription = cms.untracked.string("Save_No_C_B.xml"),
			loadState = cms.untracked.bool(False),
			saveState = cms.untracked.bool(False)
		)
	)
)

process.p = cms.Path(process.CombinedSVV2Trainer)
