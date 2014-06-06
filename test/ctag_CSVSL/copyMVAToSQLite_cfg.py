import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

# orig. version when combaining the C vs DUSG and C vs B
# process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
# 		CombinedSVRecoVertexNoSoftLepton = cms.string('tmpRecoVertexNoSoftLepton/CombinedSVMVA_RecoVertexNoSoftLepton.mva'), 
# 		CombinedSVPseudoVertexNoSoftLepton = cms.string('tmpPseudoVertexNoSoftLepton/CombinedSVMVA_PseudoVertexNoSoftLepton.mva'), 
# 		CombinedSVNoVertexNoSoftLepton = cms.string('tmpNoVertexNoSoftLepton/CombinedSVMVA_NoVertexNoSoftLepton.mva'),
# 		CombinedSVRecoVertexSoftMuon = cms.string('tmpRecoVertexSoftMuon/CombinedSVMVA_RecoVertexSoftMuon.mva'), 
# 		CombinedSVPseudoVertexSoftMuon = cms.string('tmpPseudoVertexSoftMuon/CombinedSVMVA_PseudoVertexSoftMuon.mva'), 
# 		CombinedSVNoVertexSoftMuon = cms.string('tmpNoVertexSoftMuon/CombinedSVMVA_NoVertexSoftMuon.mva'),
# 		CombinedSVRecoVertexSoftElectron = cms.string('tmpRecoVertexSoftElectron/CombinedSVMVA_RecoVertexSoftElectron.mva'), 
# 		CombinedSVPseudoVertexSoftElectron = cms.string('tmpPseudoVertexSoftElectron/CombinedSVMVA_PseudoVertexSoftElectron.mva'), 
# 		CombinedSVNoVertexSoftElectron = cms.string('tmpNoVertexSoftElectron/CombinedSVMVA_NoVertexSoftElectron.mva')
# )

process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	CombinedSVRecoVertex = cms.string('../../CalibrationRecords/CombinedSVRecoVertex.mva'), 
	CombinedSVPseudoVertex = cms.string('../../CalibrationRecords/CombinedSVPseudoVertex.mva'), 
	CombinedSVNoVertex = cms.string('../../CalibrationRecords/CombinedSVNoVertex.mva'), 
	CombinedSVIVFV2RecoVertex = cms.string('../../CalibrationRecords/CombinedSVIVFV2RecoVertex.mva'), 
	CombinedSVIVFV2PseudoVertex = cms.string('../../CalibrationRecords/CombinedSVIVFV2PseudoVertex.mva'), 
	CombinedSVIVFV2NoVertex = cms.string('../../CalibrationRecords/CombinedSVIVFV2NoVertex.mva'), 
	CombinedSVRecoVertexNoSoftLepton = cms.string('../../CalibrationRecords/CombinedRecoVertexNoSoftLepton.mva'), 
	CombinedSVPseudoVertexNoSoftLepton = cms.string('../../CalibrationRecords/CombinedPseudoVertexNoSoftLepton.mva'), 
	CombinedSVNoVertexNoSoftLepton = cms.string('../../CalibrationRecords/CombinedNoVertexNoSoftLepton.mva'), 
	CombinedSVRecoVertexSoftMuon = cms.string('../../CalibrationRecords/CombinedRecoVertexSoftMuon.mva'), 
	CombinedSVPseudoVertexSoftMuon = cms.string('../../CalibrationRecords/CombinedPseudoVertexSoftMuon.mva'), 
	CombinedSVNoVertexSoftMuon = cms.string('../../CalibrationRecords/CombinedNoVertexSoftMuon.mva'), 
	CombinedSVRecoVertexSoftElectron = cms.string('../../CalibrationRecords/CombinedRecoVertexSoftElectron.mva'), 
	CombinedSVPseudoVertexSoftElectron = cms.string('../../CalibrationRecords/CombinedPseudoVertexSoftElectron.mva'), 
	CombinedSVNoVertexSoftElectron = cms.string('../../CalibrationRecords/CombinedNoVertexSoftElectron.mva'), 
		CtagCombinedSVRecoVertexNoSoftLepton = cms.string('tmpRecoVertexNoSoftLepton_C_DUSG/tmp.mva'), 
		CtagCombinedSVPseudoVertexNoSoftLepton = cms.string('tmpPseudoVertexNoSoftLepton_C_DUSG/tmp.mva'), 
		CtagCombinedSVNoVertexNoSoftLepton = cms.string('tmpNoVertexNoSoftLepton_C_DUSG/tmp.mva'),
		CtagCombinedSVRecoVertexSoftMuon = cms.string('tmpRecoVertexSoftMuon_C_DUSG/tmp.mva'), 
		CtagCombinedSVPseudoVertexSoftMuon = cms.string('tmpPseudoVertexSoftMuon_C_DUSG/tmp.mva'), 
		CtagCombinedSVNoVertexSoftMuon = cms.string('tmpNoVertexSoftMuon_C_DUSG/tmp.mva'),
		CtagCombinedSVRecoVertexSoftElectron = cms.string('tmpRecoVertexSoftElectron_C_DUSG/tmp.mva'), 
		CtagCombinedSVPseudoVertexSoftElectron = cms.string('tmpPseudoVertexSoftElectron_C_DUSG/tmp.mva'), 
		CtagCombinedSVNoVertexSoftElectron = cms.string('tmpNoVertexSoftElectron_C_DUSG/tmp.mva'),
	CtagCombinedSVIVFV2RecoVertex = cms.string('../MVAfiles/CombinedSVV2RecoVertex_IVFnoNI_cuts.mva'), 
	CtagCombinedSVIVFV2PseudoVertex = cms.string('../MVAfiles/CombinedSVV2PseudoVertex_IVFnoNI_cuts.mva'), 
	CtagCombinedSVIVFV2NoVertex = cms.string('../MVAfiles/CombinedSVV2NoVertex_IVFnoNI_cuts.mva') 
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
		'CombinedSVIVFV2RecoVertex', 
		'CombinedSVIVFV2PseudoVertex', 
		'CombinedSVIVFV2NoVertex', 
		'CombinedSVRecoVertexNoSoftLepton', 
		'CombinedSVPseudoVertexNoSoftLepton', 
		'CombinedSVNoVertexNoSoftLepton', 
		'CombinedSVRecoVertexSoftMuon', 
		'CombinedSVPseudoVertexSoftMuon', 
		'CombinedSVNoVertexSoftMuon', 
		'CombinedSVRecoVertexSoftElectron', 
		'CombinedSVPseudoVertexSoftElectron', 
		'CombinedSVNoVertexSoftElectron', 
		'CtagCombinedSVRecoVertexNoSoftLepton', 
		'CtagCombinedSVPseudoVertexNoSoftLepton', 
		'CtagCombinedSVNoVertexNoSoftLepton',
		'CtagCombinedSVRecoVertexSoftMuon', 
		'CtagCombinedSVPseudoVertexSoftMuon', 
		'CtagCombinedSVNoVertexSoftMuon',
		'CtagCombinedSVRecoVertexSoftElectron', 
		'CtagCombinedSVPseudoVertexSoftElectron', 
		'CtagCombinedSVNoVertexSoftElectron',
		'CtagCombinedSVIVFV2RecoVertex', 
		'CtagCombinedSVIVFV2PseudoVertex', 
		'CtagCombinedSVIVFV2NoVertex' 
	)
)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)
