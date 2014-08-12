import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	CombinedSVIVFV2RecoVertex = cms.string('tmpRecoVertex_BB_B/tmp.mva'),
        CombinedSVIVFV2PseudoVertex = cms.string('tmpPseudoVertex_BB_B/tmp.mva'),
        CombinedSVIVFV2NoVertex = cms.string('tmpNoVertex_BB_B/tmp.mva'),
)
#process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	#CombinedSVIVFV2RecoVertex = cms.string('../CalibrationRecords/CombinedSVIVFV2RecoVertex.mva'),
        #CombinedSVIVFV2PseudoVertex = cms.string('../CalibrationRecords/CombinedSVIVFV2PseudoVertex.mva'),
        #CombinedSVIVFV2NoVertex = cms.string('../CalibrationRecords/CombinedSVIVFV2NoVertex.mva'),
#)
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:Validation/MVAJetTags_UNCOMBINED_xtraPtBinBBvsB_CA8.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)

process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	toPut = cms.vstring(),
	toCopy = cms.vstring(
	 'CombinedSVIVFV2RecoVertex',
         'CombinedSVIVFV2PseudoVertex',
         'CombinedSVIVFV2NoVertex',
	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)






