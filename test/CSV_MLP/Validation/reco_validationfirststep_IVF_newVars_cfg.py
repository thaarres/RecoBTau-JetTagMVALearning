import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

#keep the logging output to a nice level
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = "START53_V26::All"

# DQM include
process.load("Configuration.EventContent.EventContent_cff")
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.MessageLogger.cerr.threshold = 'ERROR'

process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
	process.CondDBSetup,
	timetype = cms.string('runnumber'),
	toGet = cms.VPSet(cms.PSet(
		record = cms.string('BTauGenericMVAJetTagComputerRcd'),
                tag = cms.string('MVAJetTags')
	)),
	connect = cms.string("sqlite_file:MVAJetTags.db"),
	#connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
	BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

# write DQM file
process.DQMoutput = cms.OutputModule("PoolOutputModule",
  splitLevel = cms.untracked.int32(0),
  outputCommands = process.DQMEventContent.outputCommands,
  fileName = cms.untracked.string('DQMfile.root'),
  #fileName = cms.untracked.string('DQMfile.root'),
  dataset = cms.untracked.PSet(
    filterName = cms.untracked.string(''),
    dataTier = cms.untracked.string('')
  )
)




#define you jet ID
jetID = cms.InputTag("ak5PFJets")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = jetID
                                                  )

#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

from RecoBTag.Configuration.RecoBTag_cff import *

#for Inclusive Vertex Finder
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
process.load('RecoBTag/SecondaryVertex/inclusiveSecondaryVertexFinderTagInfos_cfi')
process.inclusiveVertexFinder.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")
process.trackVertexArbitrator.primaryVertices = cms.InputTag("goodOfflinePrimaryVertices")

#added this block for IVF...
process.combinedSecondaryVertexNN=process.combinedSecondaryVertexV2.clone(
	calibrationRecords = cms.vstring(
		'CombinedSVV2RecoVertex',
		'CombinedSVV2PseudoVertex',
		'CombinedSVV2NoVertex'
	)
)
process.myIVFCombinedSecondaryVertexBJetTags = process.combinedSecondaryVertexV2BJetTags.clone(
  jetTagComputer = cms.string('combinedSecondaryVertexNN'),
  tagInfos = cms.VInputTag(cms.InputTag("impactParameterTagInfos"),
                           cms.InputTag("inclusiveSecondaryVertexFinderTagInfos"))
)

#new input for impactParameterTagInfos
process.IVFbtagging = cms.Sequence(
impactParameterTagInfos * 
inclusiveSecondaryVertexFinderTagInfos * 
process.myIVFCombinedSecondaryVertexBJetTags)

process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")

#do the matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()

#standard validation tools
from DQMOffline.RecoB.bTagCommon_cff import*
process.load("DQMOffline.RecoB.bTagCommon_cff")
#process.bTagCommonBlock.ptRecJetMin = cms.double(600.0)
process.bTagCommonBlock.ptRanges = cms.vdouble(0.0,40.0,60.0,90.0, 150.0,400.0,600.0,3000.0)
process.bTagCommonBlock.etaRanges = cms.vdouble(0.0, 1.2, 2.1, 2.4)

from Validation.RecoB.bTagAnalysis_cfi import *
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.bTagValidation.jetMCSrc = 'jetFlavourInfosAK5PFJets'
process.bTagValidation.allHistograms = True 
#process.bTagValidation.fastMC = True

process.CustombTagValidation = process.bTagValidation.clone(
    tagConfig = cms.VPSet(
        cms.PSet(
				    parameters = cms.PSet(
        			discriminatorStart = cms.double(-0.05),
        			discriminatorEnd = cms.double(1.05),
        			nBinEffPur = cms.int32(200),
        			# the constant b-efficiency for the differential plots versus pt and eta
        			effBConst = cms.double(0.5),
        			endEffPur = cms.double(1.005),
        			startEffPur = cms.double(-0.005)
    				),
            label = cms.InputTag("myIVFCombinedSecondaryVertexBJetTags"),
            folder = cms.string("CSV")
        ) 
			),
      finalizePlots = False,
      finalizeOnly = False
)



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)

process.btagDQM = cms.Path(
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK5PFJets *
process.goodOfflinePrimaryVertices * 
process.inclusiveVertexing * 
###process.inclusiveMergedVerticesFiltered *   
###process.bToCharmDecayVertexMerged *  
process.myak5JetTracksAssociatorAtVertex *
process.IVFbtagging * 
process.CustombTagValidation
)

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(
  process.btagDQM,
  process.endjob_step,
  process.DQMoutput_step
)

process.PoolSource.fileNames = [
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FED775BD-B8E1-E111-8ED5-003048C69036.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FEC90779-74E1-E111-A432-0025901D493E.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FE4C2F81-D0E1-E111-9080-0030487E0A2D.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FCE9FDAC-59E1-E111-82BB-0030487E5247.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FCB7FB42-ACE1-E111-B8AB-0025901D4936.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FC59218E-8AE1-E111-9934-0030487E52A3.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FADE7E47-CDE1-E111-8069-003048D4610C.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FAC4233F-73E1-E111-A13B-0030487D5D6B.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA816D44-C6E1-E111-B47A-003048C64787.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA36E77C-AFE1-E111-BAF8-003048D436B2.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA143F69-BAE1-E111-8800-003048D462DA.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA1056FA-06E2-E111-BE82-0030487EBB25.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F8F1EF6B-8BE1-E111-A6FB-003048C690A2.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F831AD2B-83E1-E111-9C92-0025901D4B06.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F6ED9CF8-B6E1-E111-BE3E-0030487FA4CB.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F6D62791-78E1-E111-A2D2-0030487FA4C5.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F69BFC11-F4E1-E111-B266-003048D4385C.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F68304EB-02E2-E111-8675-003048C676E0.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F67EE728-6FE1-E111-8DD3-0025901D4D6C.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F63D7E66-C2E1-E111-88EF-00266CF332B4.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F617F5BD-B0E1-E111-9ED8-003048D436D4.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F612958F-85E1-E111-BF68-0025904B1448.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F60F0652-C8E1-E111-BE82-002481E94B26.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F4DB115D-BFE1-E111-B89D-003048C68F6A.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F2F77AE6-20E2-E111-98FF-0030487FA623.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F2C7A257-D1E1-E111-8FE8-003048D43958.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F2BEE82F-8FE1-E111-B4BA-0030487D8563.root',
       '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F26C7F71-8BE1-E111-BC78-003048D3CD92.root',
  ]
