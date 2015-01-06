import FWCore.ParameterSet.Config as cms

process = cms.Process("IPTrainer")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.CombinedSVV2Trainer = cms.EDAnalyzer("JetTagMVATreeTrainer",
	useCategories		= cms.bool(False),
	calibrationRecord	= cms.string("CombinedSVV2PseudoVertex"),
	ignoreFlavours		= cms.vint32(0, 5, 7),
	signalFlavours		= cms.vint32(9),
	minimumTransverseMomentum = cms.double(15.0),
	minimumPseudoRapidity	= cms.double(0),
	maximumPseudoRapidity	= cms.double(2.5),
	useBBvsB 		= cms.bool(True),
	fileNames = cms.vstring(
		" /shome/thaarres/BBRetraining_SignalRadion_BackgroundQCD/skimmed_20k_eachptetabin_CombinedSVV2PseudoVertex_BB.root",
		" /shome/thaarres/BBRetraining_SignalRadion_BackgroundQCD/skimmed_20k_eachptetabin_CombinedSVV2PseudoVertex_CDUSG.root"
	)
)

process.looper = cms.Looper("JetTagMVATrainerLooper",
	trainers = cms.VPSet(
		cms.PSet(
			calibrationRecord = cms.string("CombinedSVV2PseudoVertex"),
			trainDescription = cms.untracked.string("Save_Pseudo_BB_CDUSG.xml"),
			loadState = cms.untracked.bool(False),
			saveState = cms.untracked.bool(False)
		)
	)
)

process.p = cms.Path(process.CombinedSVV2Trainer)