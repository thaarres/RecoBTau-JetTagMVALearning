import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	CombinedMVA = cms.string('SC_CSVSL/SC_CSVSL.mva'),
        CombinedSVV2RecoVertex = cms.string('VariableExtraction/CSVMLP_CSVV2dev/CombinedSVRecoVertex.mva'), 
        CombinedSVV2PseudoVertex = cms.string('VariableExtraction/CSVMLP_CSVV2dev/CombinedSVPseudoVertex.mva'), 
        CombinedSVV2NoVertex = cms.string('VariableExtraction/CSVMLP_CSVV2dev/CombinedSVNoVertex.mva')
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:SC_CSVSL.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)

process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	toPut = cms.vstring(),
	toCopy = cms.vstring(
		'CombinedMVA', 
                'CombinedSVV2RecoVertex', 
                'CombinedSVV2PseudoVertex', 
                'CombinedSVV2NoVertex'
 	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
