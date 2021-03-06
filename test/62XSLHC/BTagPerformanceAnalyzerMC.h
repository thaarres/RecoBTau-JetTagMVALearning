#ifndef BTagPerformanceAnalyzerMC_H
#define BTagPerformanceAnalyzerMC_H

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DQMOffline/RecoB/interface/BaseBTagPlotter.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DQMOffline/RecoB/interface/BTagDifferentialPlot.h"
#include "DQMOffline/RecoB/interface/AcceptJet.h"
#include "DQMOffline/RecoB/interface/JetTagPlotter.h"
#include "DQMOffline/RecoB/interface/TagCorrelationPlotter.h"
#include "DQMOffline/RecoB/interface/BaseTagInfoPlotter.h"
#include "DQMOffline/RecoB/interface/Tools.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "FWCore/Utilities/interface/InputTag.h"
//#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfo.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourInfoMatching.h"
#include "SimDataFormats/JetMatching/interface/JetFlavour.h"

#include "DQMOffline/RecoB/interface/CorrectJet.h"
#include "DQMOffline/RecoB/interface/MatchJet.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/Common/interface/Association.h"

#include <string>
#include <vector>
#include <map>

//class CaloJetRef;

/** \class BTagPerformanceAnalyzerMC
 *
 *  Top level steering routine for b tag performance analysis.
 *
 */

class BTagPerformanceAnalyzerMC : public edm::EDAnalyzer {
   public:
      explicit BTagPerformanceAnalyzerMC(const edm::ParameterSet& pSet);

      ~BTagPerformanceAnalyzerMC();

      virtual void beginRun(const edm::Run & run, const edm::EventSetup & es);

      virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

      virtual void endJob();

   private:

  struct JetRefCompare :
       public std::binary_function<edm::RefToBase<reco::Jet>, edm::RefToBase<reco::Jet>, bool> {
    inline bool operator () (const edm::RefToBase<reco::Jet> &j1,
                             const edm::RefToBase<reco::Jet> &j2) const
    { return j1.id() < j2.id() || (j1.id() == j2.id() && j1.key() < j2.key()); }
  };

  // Get histogram plotting options from configuration.
  void bookHistos();
  EtaPtBin getEtaPtBin(const int& iEta, const int& iPt);
    typedef std::pair<reco::Jet, reco::JetFlavour> JetWithFlavour;
typedef std::map<edm::RefToBase<reco::Jet>, unsigned int, JetRefCompare> FlavourMap;
typedef std::map<edm::RefToBase<reco::Jet>, reco::JetFlavour::Leptons, JetRefCompare> LeptonMap;
  //  reco::JetFlavour getJetFlavour(
  //	edm::RefToBase<reco::Jet> caloRef, FlavourMap flavours);
  bool getJetWithFlavour(edm::RefToBase<reco::Jet> caloRef,
                         const FlavourMap& _flavours, JetWithFlavour &jetWithFlavour,
			 const edm::EventSetup & es, 
			 edm::Handle<edm::Association<reco::GenJetCollection> > genJetsMatched);
  bool getJetWithGenJet(edm::RefToBase<reco::Jet> jetRef, edm::Handle<edm::Association<reco::GenJetCollection> > genJetsMatched); 

  std::vector<std::string> tiDataFormatType;
  bool partonKinematics;
  double ptPartonMin, ptPartonMax;
  AcceptJet jetSelector;   // Decides if jet and parton satisfy kinematic cuts.
  std::vector<double> etaRanges, ptRanges;
  bool produceEps, producePs;
  std::string psBaseName, epsBaseName, inputFile;
  std::string JECsource;
  bool doJEC;
  bool update, allHisto;
  bool finalize;
  bool finalizeOnly;

  bool ptHatWeight;

  edm::InputTag jetMCSrc;
  edm::InputTag slInfoTag;
  edm::InputTag genJetsMatchedSrc;

  std::vector< std::vector<JetTagPlotter*> > binJetTagPlotters;
  std::vector< std::vector<TagCorrelationPlotter*> > binTagCorrelationPlotters;
  std::vector< std::vector<BaseTagInfoPlotter*> > binTagInfoPlotters;
  std::vector<edm::InputTag> jetTagInputTags;
  std::vector< std::pair<edm::InputTag, edm::InputTag> > tagCorrelationInputTags;
  std::vector< std::vector<edm::InputTag> > tagInfoInputTags;
  // Contains plots for each bin of rapidity and pt.
  std::vector< std::vector<BTagDifferentialPlot*> > differentialPlots;
  //  JetFlavourIdentifier jfi;
  std::vector<edm::ParameterSet> moduleConfig;
  std::map<BaseTagInfoPlotter*, size_t> binTagInfoPlottersToModuleConfig;

  std::string flavPlots_;
  unsigned int mcPlots_;
  bool makeDiffPlots_;

  CorrectJet jetCorrector;
  MatchJet jetMatcher;

  bool doPUid; 
  bool eventInitialized;
  bool electronPlots, muonPlots, tauPlots;

  //add consumes 
  edm::EDGetTokenT<GenEventInfoProduct> genToken;
  edm::EDGetTokenT<edm::Association<reco::GenJetCollection>> genJetsMatchedToken;
  edm::EDGetTokenT<reco::JetFlavourInfoMatchingCollection> jetToken;
  edm::EDGetTokenT<reco::SoftLeptonTagInfoCollection> slInfoToken;
  std::vector< edm::EDGetTokenT<reco::JetTagCollection> > jetTagToken;
  std::vector< std::pair<edm::EDGetTokenT<reco::JetTagCollection>, edm::EDGetTokenT<reco::JetTagCollection>> > tagCorrelationToken;
  std::vector<std::vector <edm::EDGetTokenT<edm::View<reco::BaseTagInfo>> >> tagInfoToken;
};


#endif
