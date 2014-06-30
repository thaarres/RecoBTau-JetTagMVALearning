import FWCore.ParameterSet.Config as cms

process = cms.Process("IPTrainer")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.CombinedSVV2Trainer = cms.EDAnalyzer("JetTagMVATreeTrainer",
	useCategories		= cms.bool(False),
	calibrationRecord	= cms.string("CombinedSVV2RecoVertex"),
	ignoreFlavours		= cms.vint32(0, 5),
	signalFlavours		= cms.vint32(4),
	minimumTransverseMomentum = cms.double(15.0),
	minimumPseudoRapidity	= cms.double(0),
	maximumPseudoRapidity	= cms.double(2.5),
	fileNames = cms.vstring(
		" /afs/cern.ch/work/p/pvmulder/public/BTagging/GIT_SETUP/TEST_RECIPE/CMSSW_5_3_13_patch3/src/RootFiles_CMSSW5313_gitrecipe/QCD/skimmed_20k_eachptetabin_CombinedSVV2RecoVertex_C.root",
		" /afs/cern.ch/work/p/pvmulder/public/BTagging/GIT_SETUP/TEST_RECIPE/CMSSW_5_3_13_patch3/src/RootFiles_CMSSW5313_gitrecipe/QCD/skimmed_20k_eachptetabin_CombinedSVV2RecoVertex_DUSG.root"
	)
)

process.looper = cms.Looper("JetTagMVATrainerLooper",
	trainers = cms.VPSet(
		cms.PSet(
			calibrationRecord = cms.string("CombinedSVV2RecoVertex"),
			trainDescription = cms.untracked.string("Save_Reco_C_DUSG.xml"),
			loadState = cms.untracked.bool(False),
			saveState = cms.untracked.bool(False)
		)
	)
)

process.p = cms.Path(process.CombinedSVV2Trainer)
