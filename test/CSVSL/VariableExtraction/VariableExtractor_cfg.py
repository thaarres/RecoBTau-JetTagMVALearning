import FWCore.ParameterSet.Config as cms

process = cms.Process("CSVTrainer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("RecoBTau.JetTagComputer.jetTagRecord_cfi")
process.load("RecoBTag.SecondaryVertex.combinedSecondaryVertexSoftLeptonES_cfi")


# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.Geometry_cff") #old one, to use for old releases
process.load("Configuration.Geometry.GeometryIdeal_cff") #new one
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.GlobalTag.globaltag = cms.string("START53_V26::All")

#define you jet ID
jetID = cms.InputTag("ak5PFJets")
JetCut=cms.string("neutralHadronEnergyFraction < 0.99 && neutralEmEnergyFraction < 0.99 && nConstituents > 1 && chargedHadronEnergyFraction > 0.0 && chargedMultiplicity > 0.0 && chargedEmEnergyFraction < 0.99")

#do the PFnoPU using PF2PAT
process.out = cms.OutputModule("PoolOutputModule",
                               outputCommands = cms.untracked.vstring('drop *'),
                               fileName = cms.untracked.string('EmptyFile.root')
                               )
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix="PF2PAT"
usePF2PAT(process,runPF2PAT=True, jetAlgo="AK5", runOnMC=True, postfix=postfix, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), typeIMetCorrections=False
#,jetCorrections=('AK5PFchs', ['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), typeIMetCorrections=False, outputModules=['out']
)
process.patJetCorrFactorsPF2PAT.payload = 'AK5PFchs'
process.patJetCorrFactorsPF2PAT.levels = cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])
process.pfPileUpPF2PAT.checkClosestZVertex = False
process.patJetsPF2PAT.discriminatorSources = cms.VInputTag(
        cms.InputTag("trackCountingHighEffBJetTagsAODPF2PAT")
)
process.btaggingJetTagsAODPF2PAT = cms.Sequence(getattr(process,"trackCountingHighEffBJetTagsAODPF2PAT") )
# top projections in PF2PAT:
getattr(process,"pfNoPileUp"+postfix).enable = True
getattr(process,"pfNoMuon"+postfix).enable = True # isolated muon is removed from jet clustering
getattr(process,"pfNoElectron"+postfix).enable = True # isolated electron is removed from jet clustering
process.selectedPatJetsPF2PAT.cut = JetCut
process.JECAlgo = cms.Sequence( getattr(process,"patPF2PATSequence"+postfix) )

newjetID=cms.InputTag("selectedPatJetsPF2PAT")

#JTA for your jets
from RecoJets.JetAssociationProducers.j2tParametersVX_cfi import *
process.myak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
                                                  j2tParametersVX,
                                                  jets = newjetID
                                                  )

#new input for impactParameterTagInfos
from RecoBTag.Configuration.RecoBTag_cff import *
process.impactParameterTagInfos.jetTracks = cms.InputTag("myak5JetTracksAssociatorAtVertex")


#input for softLeptonTagInfos
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')
process.softPFElectronsTagInfos.jets = newjetID
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag('goodOfflinePrimaryVertices')
process.softPFMuonsTagInfos.jets = newjetID #we need to be absolutely sure that the CHS is applied... maybe we should get rid of PAT?


process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi")  
process.AK5byRef.jets = newjetID

#do the matching
process.flavourSeq = cms.Sequence(
    process.myPartons *
    process.AK5Flavour
    )

#select good primary vertex
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

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
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVRecoVertexNoSoftLepton"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVPseudoVertexNoSoftLepton"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVNoVertexNoSoftLepton"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity"
)), # no trackEtaRel!!!???!!!
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVRecoVertexSoftMuon"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVPseudoVertexSoftMuon"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVNoVertexSoftMuon"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)), # no trackEtaRel!!!???!!!
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVRecoVertexSoftElectron"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","flightDistance2dSig","flightDistance3dSig","flightDistance2dVal","flightDistance3dVal","trackSumJetEtRatio","jetNSecondaryVertices","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","vertexFitProb","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVPseudoVertexSoftElectron"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackEtaRel","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","vertexMass","vertexNTracks","vertexEnergyRatio","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","vertexJetDeltaR","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","massVertexEnergyFraction","vertexBoostOverSqrtJetPt","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)),
		cms.untracked.PSet( label = cms.untracked.string("CombinedSVNoVertexSoftElectron"),  variables=cms.untracked.vstring(
"jetPt","jetEta","vertexCategory","vertexLeptonCategory","trackSip2dSig","trackSip3dSig","trackSip2dVal","trackSip3dVal","trackPtRel","trackPPar","trackDeltaR","trackPtRatio","trackPParRatio","trackJetDist","trackDecayLenVal","trackSip2dSigAboveCharm","trackSip3dSigAboveCharm","trackSumJetEtRatio","trackSumJetDeltaR","jetNTracks","trackSip2dValAboveCharm","trackSip3dValAboveCharm","chargedHadronEnergyFraction","neutralHadronEnergyFraction","photonEnergyFraction","electronEnergyFraction","muonEnergyFraction","chargedHadronMultiplicity","neutralHadronMultiplicity","photonMultiplicity","electronMultiplicity","muonMultiplicity","hadronMultiplicity","hadronPhotonMultiplicity","totalMultiplicity","leptonPtRel","leptonSip3d","leptonDeltaR","leptonRatioRel","leptonP0Par","leptonEtaRel","leptonRatio"
)) # no trackEtaRel!!!???!!!


	),
	ipTagInfos = cms.InputTag("impactParameterTagInfos"),
	svTagInfos =cms.InputTag("secondaryVertexTagInfos"),
	muonTagInfos =cms.InputTag("softPFMuonsTagInfos"),
	elecTagInfos =cms.InputTag("softPFElectronsTagInfos"),
	
	minimumTransverseMomentum = cms.double(15.0),
	useCategories = cms.bool(True),
  calibrationRecords = cms.vstring(
		'CombinedSVRecoVertexNoSoftLepton', 
		'CombinedSVPseudoVertexNoSoftLepton', 
		'CombinedSVNoVertexNoSoftLepton',
		'CombinedSVRecoVertexSoftMuon', 
		'CombinedSVPseudoVertexSoftMuon', 
		'CombinedSVNoVertexSoftMuon',
		'CombinedSVRecoVertexSoftElectron', 
		'CombinedSVPseudoVertexSoftElectron', 
		'CombinedSVNoVertexSoftElectron'),
	categoryVariableName = cms.string('vertexLeptonCategory'), # vertexCategory = Reco,Pseudo,No
#  calibrationRecords = cms.vstring(
#		'CombinedSVRecoVertex', 
#		'CombinedSVPseudoVertex', 
#		'CombinedSVNoVertex'),
#	categoryVariableName = cms.string('vertexCategory'), # vertexCategory = Reco,Pseudo,No
	maximumPseudoRapidity = cms.double(2.5),
	signalFlavours = cms.vint32(5, 7),
	minimumPseudoRapidity = cms.double(0.0),
	jetTagComputer = cms.string('combinedSecondaryVertexSoftLepton'),
	jetFlavourMatching = cms.InputTag("AK5byValAlgo"),
	ignoreFlavours = cms.vint32(0)
)

process.p = cms.Path(
process.goodOfflinePrimaryVertices * 
process.JECAlgo * 
process.myak5JetTracksAssociatorAtVertex * 
process.impactParameterTagInfos * 
process.secondaryVertexTagInfos * 
process.softPFMuonsTagInfos *
process.softPFElectronsTagInfos *
process.flavourSeq *  
process.combinedSVMVATrainer 
)

 
