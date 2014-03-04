import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")


# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff") #new one
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("START53_V26::All")

#To use the newest training!
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.BTauMVAJetTagComputerRecord = cms.ESSource("PoolDBESSource",
       process.CondDBSetup,
       timetype = cms.string('runnumber'),
       toGet = cms.VPSet(cms.PSet(
               record = cms.string('BTauGenericMVAJetTagComputerRcd'),
               tag = cms.string('MVAJetTags')
       )),
       connect = cms.string("sqlite_file:MVAJetTags_CSVV2dev.db"),
       #connect = cms.string('frontier://FrontierDev/CMS_COND_BTAU'),
       BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService')
)
process.es_prefer_BTauMVAJetTagComputerRecord = cms.ESPrefer("PoolDBESSource","BTauMVAJetTagComputerRecord")

process.load("RecoBTag.SecondaryVertex.combinedSecondaryVertexES_cfi")
process.combinedSecondaryVertexV2.calibrationRecords = cms.vstring(
		'CombinedSVV2RecoVertex', 
		'CombinedSVV2PseudoVertex', 
		'CombinedSVV2NoVertex')

process.load("RecoBTau.JetTagComputer.combinedMVAES_cfi")
process.combinedMVA.jetTagComputers = cms.VPSet(
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('jetProbability')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('combinedSecondaryVertexV2')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFMuon')
		),
		cms.PSet(
			discriminator = cms.bool(True),
			variables = cms.bool(False),
			jetTagComputer = cms.string('softPFElectron')
		)
)



#define you jet ID
jetID = cms.InputTag("ak5PFJets")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = newjetID 
                                                  )
#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")

#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

#input for softLeptonTagInfos
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
#process.jetFlavourInfosAK5PFJets.jets = newjetID


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(11)
)

process.source = cms.Source("PoolSource",
	skipEvents=cms.untracked.uint32(0),
	fileNames = cms.untracked.vstring(
#'/store/mc/Fall11/QCD_Pt-50to80_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00225C27-4744-E111-8583-003048C692E4.root',
#'/store/mc/Fall11/QCD_Pt-80to120_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00D668C4-5244-E111-A8F6-0025901D4936.root',
#'/store/mc/Fall11/QCD_Pt-120to170_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/023CE3AD-CF46-E111-90CB-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-170to300_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0433579C-7644-E111-9D93-00215AD4D6C8.root',
#'/store/mc/Fall11/QCD_Pt-300to470_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00C128DE-923F-E111-AA76-003048C69312.root',
#'/store/mc/Fall11/QCD_Pt-470to600_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/00CC4BA4-FC45-E111-A993-003048F0E80C.root',
#'/store/mc/Fall11/QCD_Pt-600to800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/000548D5-0A40-E111-A327-002481E0DA4E.root',
#'/store/mc/Fall11/QCD_Pt-800to1000_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0469BF65-8343-E111-8E43-003048F0E3B2.root',
#'/store/mc/Fall11/QCD_Pt-1000to1400_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/14151191-9043-E111-BA90-003048C690A0.root',
#'/store/mc/Fall11/QCD_Pt-1400to1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0E10C938-1146-E111-95AC-0025901D4A58.root',
#'/store/mc/Fall11/QCD_Pt-1800_Tune4C_7TeV_pythia8/AODSIM/PU_S6_START44_V9B-v1/0000/0C4D9605-2544-E111-B39F-003048D4DF80.root',
'/store/mc/Summer12/QCD_Pt-15to3000_TuneZ2_Flat_8TeV_pythia6/AODSIM/PU_S7_START52_V9-v1/0000/02FE9503-3C97-E111-915E-0030487D5D5B.root'
	)
)


# to write out events
#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('outfile.root')
#)

# write out file
#process.output = cms.EndPath(
#  process.out
#)


process.superCombinedTrainer = cms.EDAnalyzer("JetTagMVAExtractor",
	variables = cms.untracked.VPSet( cms.untracked.PSet(
		label = cms.untracked.string("combinedMVA"),  
		variables=cms.untracked.vstring("jetPt","jetEta","algoDiscriminator")
	)),

  jetTagComputers = cms.VPSet(
         cms.PSet(
             discriminator = cms.bool(True),
             variables = cms.bool(False),
             jetTagComputer = cms.string('jetProbability')
         ),
         cms.PSet(
             discriminator = cms.bool(True),
             variables = cms.bool(False),
             jetTagComputer = cms.string('combinedSecondaryVertexV2')
         ),
         cms.PSet(
             discriminator = cms.bool(True),
             variables = cms.bool(False),
             jetTagComputer = cms.string('softPFMuon')
         ),
         cms.PSet(
             discriminator = cms.bool(True),
             variables = cms.bool(False),
             jetTagComputer = cms.string('softPFElectron')
         )
 ),
	
  ipTagInfos = cms.InputTag("impactParameterTagInfos"),
  svTagInfos = cms.InputTag("secondaryVertexTagInfos"),
	smTagInfos = cms.InputTag("softPFMuonsTagInfos"),
	seTagInfos = cms.InputTag("softPFElectronsTagInfos"),

	useCategories = cms.bool(False),
  calibrationRecord = cms.string('combinedMVA'),

	minimumTransverseMomentum = cms.double(15.0),
	maximumTransverseMomentum = cms.double(9999999.),
	minimumPseudoRapidity = cms.double(0.0),
	maximumPseudoRapidity = cms.double(2.5),
	signalFlavours = cms.vint32(5, 7),
	jetTagComputer = cms.string('combinedMVA'),
	jetFlavourMatching = cms.InputTag("jetFlavourInfosAK5PFJets"),
	ignoreFlavours = cms.vint32(0)
)


process.p = cms.Path(
process.goodOfflinePrimaryVertices *
process.myak5JetTracksAssociatorAtVertex *
process.impactParameterTagInfos *
process.secondaryVertexTagInfos *
process.softPFMuonsTagInfos *
process.softPFElectronsTagInfos *
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK5PFJets *
process.superCombinedTrainer 
)


 
