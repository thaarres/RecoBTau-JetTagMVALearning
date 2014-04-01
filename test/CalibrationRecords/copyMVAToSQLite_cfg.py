import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	CombinedSVRecoVertex = cms.string('CombinedSVRecoVertex.mva'), 
	CombinedSVPseudoVertex = cms.string('CombinedSVPseudoVertex.mva'), 
	CombinedSVNoVertex = cms.string('CombinedSVNoVertex.mva'), 
	CombinedSVV1RecoVertex = cms.string('CombinedSVV1RecoVertex.mva'), 
	CombinedSVV1PseudoVertex = cms.string('CombinedSVV1PseudoVertex.mva'), 
	CombinedSVV1NoVertex = cms.string('CombinedSVV1NoVertex.mva'), 
	CombinedSVIVFV1RecoVertex = cms.string('CombinedSVIVFV1RecoVertex.mva'), 
	CombinedSVIVFV1PseudoVertex = cms.string('CombinedSVIVFV1PseudoVertex.mva'), 
	CombinedSVIVFV1NoVertex = cms.string('CombinedSVIVFV1NoVertex.mva'), 
	CombinedSVV2RecoVertex = cms.string('CombinedSVV2RecoVertex.mva'), 
	CombinedSVV2PseudoVertex = cms.string('CombinedSVV2PseudoVertex.mva'), 
	CombinedSVV2NoVertex = cms.string('CombinedSVV2NoVertex.mva'), 
	CombinedSVRecoVertexNoSoftLepton = cms.string('CombinedRecoVertexNoSoftLepton.mva'), 
	CombinedSVPseudoVertexNoSoftLepton = cms.string('CombinedPseudoVertexNoSoftLepton.mva'), 
	CombinedSVNoVertexNoSoftLepton = cms.string('CombinedNoVertexNoSoftLepton.mva'), 
	CombinedSVRecoVertexSoftMuon = cms.string('CombinedRecoVertexSoftMuon.mva'), 
	CombinedSVPseudoVertexSoftMuon = cms.string('CombinedPseudoVertexSoftMuon.mva'), 
	CombinedSVNoVertexSoftMuon = cms.string('CombinedNoVertexSoftMuon.mva'), 
	CombinedSVRecoVertexSoftElectron = cms.string('CombinedRecoVertexSoftElectron.mva'), 
	CombinedSVPseudoVertexSoftElectron = cms.string('CombinedPseudoVertexSoftElectron.mva'), 
	CombinedSVNoVertexSoftElectron = cms.string('CombinedNoVertexSoftElectron.mva'), 
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:MVAJetTags.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)

process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	toPut = cms.vstring(),
	toCopy = cms.vstring(
		'CombinedSVRecoVertex', 
		'CombinedSVPseudoVertex', 
		'CombinedSVNoVertex', 
		'CombinedSVV1RecoVertex', 
		'CombinedSVV1PseudoVertex', 
		'CombinedSVV1NoVertex', 
		'CombinedSVIVFV1RecoVertex', 
		'CombinedSVIVFV1PseudoVertex', 
		'CombinedSVIVFV1NoVertex', 
		'CombinedSVV2RecoVertex', 
		'CombinedSVV2PseudoVertex', 
		'CombinedSVV2NoVertex', 
		'CombinedSVRecoVertexNoSoftLepton', 
		'CombinedSVPseudoVertexNoSoftLepton', 
		'CombinedSVNoVertexNoSoftLepton', 
		'CombinedSVRecoVertexSoftMuon', 
		'CombinedSVPseudoVertexSoftMuon', 
		'CombinedSVNoVertexSoftMuon', 
		'CombinedSVRecoVertexSoftElectron', 
		'CombinedSVPseudoVertexSoftElectron', 
		'CombinedSVNoVertexSoftElectron', 
	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
