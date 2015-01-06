import FWCore.ParameterSet.Config as cms

process = cms.Process("MVAJetTagsSQLiteSave")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

#TO COMPARE ALL TAGGERS, USE THIS
process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	CombinedSVRecoVertex = cms.string('CalibrationRecords/CombinedSVRecoVertex.mva'),
	CombinedSVPseudoVertex = cms.string('CalibrationRecords/CombinedSVPseudoVertex.mva'),
	CombinedSVNoVertex = cms.string('CalibrationRecords/CombinedSVNoVertex.mva'),
	CombinedSVIVFV2RecoVertex = cms.string('CalibrationRecords/CombinedSVIVFV2RecoVertex.mva'),
	CombinedSVIVFV2PseudoVertex = cms.string('CalibrationRecords/CombinedSVIVFV2PseudoVertex.mva'),
	CombinedSVIVFV2NoVertex = cms.string('CalibrationRecords/CombinedSVIVFV2NoVertex.mva'),
	NEWCombinedSVIVFV2RecoVertex = cms.string('BBtag_CSVMLPIVF/tmpRecoVertex_B_BB/RecoVertex_B_BB.mva'),
        NEWCombinedSVIVFV2NoVertex = cms.string('BBtag_CSVMLPIVF/tmpNoVertex_B_BB/NoVertex_B_BB.mva'),
        NEWCombinedSVIVFV2PseudoVertex = cms.string('BBtag_CSVMLPIVF/tmpPseudoVertex_B_BB/PseudoVertex_B_BB.mva'),
        NEWCombinedSVIVFV2RecoRecoVertex = cms.string('BBtag_CSVMLPIVF/tmpRecoRecoVertex_B_BB/RecoRecoVertex_B_BB.mva')
)

##TO ONLY LOOK AT CSVIVFV2, USE THIS
#process.calib = cms.ESSource("BTauGenericMVAJetTagComputerFileSource",
	#CombinedSVIVFV2RecoVertex = cms.string('CSV_MLP/tmpRecoVertex/CombinedSVV2MVA_RecoVertex.mva'), 
	#CombinedSVIVFV2PseudoVertex = cms.string('CSV_MLP/tmpPseudoVertex/CombinedSVV2MVA_PseudoVertex.mva'), 
	#CombinedSVIVFV2NoVertex = cms.string('CSV_MLP/tmpNoVertex/CombinedSVV2MVA_NoVertex.mva'), 
#)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
	DBParameters = cms.PSet( messageLevel = cms.untracked.int32(0) ),
	timetype = cms.untracked.string('runnumber'),
	connect = cms.string('sqlite_file:MVAJetTags_Radion_V1.db'),
	toPut = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
		tag = cms.string('MVAJetTags')
	))
)


#TO COMPARE ALL TAGGERS, USE THIS
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
              'NEWCombinedSVIVFV2NoVertex',
              'NEWCombinedSVIVFV2PseudoVertex',
              'NEWCombinedSVIVFV2RecoRecoVertex'
     )
)
     
##TO ONLY LOOK AT CSVIVFV2, USE THIS
#process.jetTagMVATrainerSave = cms.EDAnalyzer("JetTagMVATrainerSave",
	#toPut = cms.vstring(),
	#toCopy = cms.vstring(
		#'CombinedSVIVFV2RecoVertex', 
		#'CombinedSVIVFV2PseudoVertex', 
		#'CombinedSVIVFV2NoVertex', 
	#)
#)

process.outpath = cms.EndPath(process.jetTagMVATrainerSave)





