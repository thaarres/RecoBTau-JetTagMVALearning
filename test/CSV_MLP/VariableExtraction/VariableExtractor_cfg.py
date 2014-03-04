import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")
process.load("RecoBTag.SecondaryVertex.combinedSecondaryVertexES_cfi")


# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff") #new one
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("START53_V26::All")

#define you jet ID
jetID = cms.InputTag("ak5PFJets")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = jetID
                                                  )

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")

#for the flavour matching
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone()

from PhysicsTools.JetMCAlgos.AK5PFJetsMCFlavourInfos_cfi import ak5JetFlavourInfos
process.jetFlavourInfosAK5PFJets = ak5JetFlavourInfos.clone()
#process.jetFlavourInfosAK5PFJets.jets = newjetID

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(101)
)

process.source = cms.Source("PoolSource",
#	fileNames = cms.untracked.vstring('file:testTagInfos.root')
	fileNames = cms.untracked.vstring(
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/001C868B-B2E1-E111-9BE3-003048D4DCD8.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0046E17E-BCE1-E111-A1D1-003048F02CB2.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0076C8E3-9AE1-E111-917C-003048D439AA.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0244AEA1-7CE1-E111-956B-0025901D4C3C.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/024A37B1-C9E1-E111-9CDF-0025901D4B04.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/027E3BA0-F2E1-E111-AAD3-003048D3CA06.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02963472-F6E1-E111-B0F9-0030487D814D.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A13705-B0E1-E111-8248-0030487E4EB5.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A9D360-C9E1-E111-B4AE-003048D3CA06.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02F5A838-8FE1-E111-B0C8-00266CFFA654.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02FDED20-B9E1-E111-B985-0030487D5EBD.root',
'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/040B9556-C2E1-E111-A7F7-00266CF1074C.root',

	)
)

process.combinedSVMVATrainer = cms.EDAnalyzer("JetTagMVAExtractor",
	variables = cms.untracked.VPSet(
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2RecoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2PseudoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),

		cms.untracked.PSet( label = cms.untracked.string("CombinedSVV2NoVertex"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity"
)) # no trackEtaRel!!!???!!!


	),
	ipTagInfos = cms.InputTag("impactParameterTagInfos"),
	svTagInfos =cms.InputTag("secondaryVertexTagInfos"),
	
	minimumTransverseMomentum = cms.double(15.0),
	useCategories = cms.bool(True),
        calibrationRecords = cms.vstring(
                'CombinedSVV2RecoVertex',
                'CombinedSVV2PseudoVertex',
                'CombinedSVV2NoVertex'),
	categoryVariableName = cms.string('vertexCategory'), # vertexCategory = Reco,Pseudo,No
	maximumPseudoRapidity = cms.double(2.5),
	signalFlavours = cms.vint32(5, 7),
	minimumPseudoRapidity = cms.double(0.0),
	jetTagComputer = cms.string('combinedSecondaryVertexV2'),
	jetFlavourMatching = cms.InputTag("jetFlavourInfosAK5PFJets"),
	ignoreFlavours = cms.vint32(0)
)

process.p = cms.Path(
process.myak5JetTracksAssociatorAtVertex * 
process.impactParameterTagInfos * 
process.secondaryVertexTagInfos * 
process.selectedHadronsAndPartons *
process.jetFlavourInfosAK5PFJets *
process.combinedSVMVATrainer 
)

 
