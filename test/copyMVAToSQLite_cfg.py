import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

#process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	#CombinedSVRecoVertex = cms.string('CSV_MLP/tmpRecoVertex/CombinedSVV2MVA_RecoVertex.mva'), 
	#CombinedSVPseudoVertex = cms.string('CSV_MLP/tmpPseudoVertex/CombinedSVV2MVA_PseudoVertex.mva'), 
	#CombinedSVNoVertex = cms.string('CSV_MLP/tmpNoVertex/CombinedSVV2MVA_NoVertex.mva'), 
#)
process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
     CombinedSVRecoVertex =
cms.string('CalibrationRecords/CombinedSVRecoVertex.mva'),
     CombinedSVPseudoVertex =
cms.string('CalibrationRecords/CombinedSVPseudoVertex.mva'),
     CombinedSVNoVertex =
cms.string('CalibrationRecords/CombinedSVNoVertex.mva'),
     CombinedSVIVFV2RecoVertex =
cms.string('CalibrationRecords/CombinedSVIVFV2RecoVertex.mva'),
     CombinedSVIVFV2PseudoVertex =
cms.string('CalibrationRecords/CombinedSVIVFV2PseudoVertex.mva'),
     CombinedSVIVFV2NoVertex =
cms.string('CalibrationRecords/CombinedSVIVFV2NoVertex.mva'),
     NEWCombinedSVIVFV2RecoVertex =
cms.string('CSV_MLP/tmpRecoVertex/CombinedSVV2MVA_RecoVertex.mva'),
     NEWCombinedSVIVFV2PseudoVertex =
cms.string('CSV_MLP/tmpRecoVertex/CombinedSVV2MVA_PseudoVertex.mva'),
     NEWCombinedSVIVFV2NoVertex =
cms.string('CSV_MLP/tmpRecoVertex/CombinedSVV2MVA_NoVertex.mva'),
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:All_MVAJetTags.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)

#process.TFileService = cms.Service("TFileService",
#                                       fileName = cms.string('MVAJetTags.db')
#                                   )


#process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	#toPut = cms.vstring(),
	#toCopy = cms.vstring(
		#'CombinedSVRecoVertex', 
		#'CombinedSVPseudoVertex', 
		#'CombinedSVNoVertex', 
	#)
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
         'NEWCombinedSVIVFV2RecoVertex',
         'NEWCombinedSVIVFV2PseudoVertex',
         'NEWCombinedSVIVFV2NoVertex',
     )
)
process.outpath = cms.EndPath(process.jetTagMVATrainerSave)






