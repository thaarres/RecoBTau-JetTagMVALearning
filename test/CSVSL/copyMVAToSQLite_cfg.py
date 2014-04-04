import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
		CombinedSVRecoVertexNoSoftLepton = cms.string('tmpRecoVertexNoSoftLepton/CombinedSVMVA_RecoVertexNoSoftLepton.mva'), 
		CombinedSVPseudoVertexNoSoftLepton = cms.string('tmpPseudoVertexNoSoftLepton/CombinedSVMVA_PseudoVertexNoSoftLepton.mva'), 
		CombinedSVNoVertexNoSoftLepton = cms.string('tmpNoVertexNoSoftLepton/CombinedSVMVA_NoVertexNoSoftLepton.mva'),
		CombinedSVRecoVertexSoftMuon = cms.string('tmpRecoVertexSoftMuon/CombinedSVMVA_RecoVertexSoftMuon.mva'), 
		CombinedSVPseudoVertexSoftMuon = cms.string('tmpPseudoVertexSoftMuon/CombinedSVMVA_PseudoVertexSoftMuon.mva'), 
		CombinedSVNoVertexSoftMuon = cms.string('tmpNoVertexSoftMuon/CombinedSVMVA_NoVertexSoftMuon.mva'),
		CombinedSVRecoVertexSoftElectron = cms.string('tmpRecoVertexSoftElectron/CombinedSVMVA_RecoVertexSoftElectron.mva'), 
		CombinedSVPseudoVertexSoftElectron = cms.string('tmpPseudoVertexSoftElectron/CombinedSVMVA_PseudoVertexSoftElectron.mva'), 
		CombinedSVNoVertexSoftElectron = cms.string('tmpNoVertexSoftElectron/CombinedSVMVA_NoVertexSoftElectron.mva')
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
		'CombinedSVRecoVertexNoSoftLepton', 
		'CombinedSVPseudoVertexNoSoftLepton', 
		'CombinedSVNoVertexNoSoftLepton',
		'CombinedSVRecoVertexSoftMuon', 
		'CombinedSVPseudoVertexSoftMuon', 
		'CombinedSVNoVertexSoftMuon',
		'CombinedSVRecoVertexSoftElectron', 
		'CombinedSVPseudoVertexSoftElectron', 
		'CombinedSVNoVertexSoftElectron'
	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
