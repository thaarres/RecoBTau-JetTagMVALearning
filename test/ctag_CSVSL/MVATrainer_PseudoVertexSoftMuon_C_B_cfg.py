import FWCore.ParameterSet.Config as cms

process = cms.Process("IPTrainer")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.combinedSVTrainer = cms.EDAnalyzer("JetTagMVATreeTrainer",
	useCategories		= cms.bool(False),
	calibrationRecord	= cms.string("CombinedSVPseudoVertexSoftMuon"),
	ignoreFlavours		= cms.vint32(0, 1, 2, 3, 21),
	signalFlavours		= cms.vint32(4),
	minimumTransverseMomentum = cms.double(15.0),
	minimumPseudoRapidity	= cms.double(0),
	maximumPseudoRapidity	= cms.double(2.5),

	factor = cms.double(1),
	bound = cms.double(50),

	fileNames = cms.vstring(
		"/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/QCD_training/skimmed_20k_eachptetabin_CombinedSVPseudoVertexSoftMuon_C.root",
		"/user/pvmulder/NewEraOfDataAnalysis/BTagServiceWork/DEVELOPMENT/RootFiles_CSVSLIVF_JetFlavourPUjetIDcleanIVF/QCD_training/skimmed_20k_eachptetabin_CombinedSVPseudoVertexSoftMuon_B.root"
	),
	weightFile = cms.string("weights/CombinedSVPseudoVertexSoftMuon_CB_histo.txt"),
	biasFiles = cms.vstring(
		"*",
		"-",
		"weights/CombinedSVPseudoVertexSoftMuon_C_B_ratio.txt"
	)
)

process.looper = cms.Looper("JetTagMVATrainerLooper",
	trainers = cms.VPSet(
		cms.PSet(
			calibrationRecord = cms.string("CombinedSVPseudoVertexSoftMuon"),
			trainDescription = cms.untracked.string("Save_PseudoVertexSoftMuon_C_B.xml"),
			loadState = cms.untracked.bool(False),
			saveState = cms.untracked.bool(False)
		)
	)
)

process.p = cms.Path(process.combinedSVTrainer)
