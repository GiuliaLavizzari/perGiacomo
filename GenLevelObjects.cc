#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

#include <vector>

#include "TFile.h"
#include "TH2D.h"
#include "TString.h"
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/VectorUtil.h"

#include <iostream>
using namespace ROOT::Math;

class GenLevelObjects : public multidraw::TTreeFunction {
public:
  GenLevelObjects();
  ~GenLevelObjects(){};

  char const* getName() const override { return "GenLevelObjects"; }
  TTreeFunction* clone() const override { return new GenLevelObjects(); }

  void setValues();
  void beginEvent(long long) override;
  unsigned getNdata() override { return outputValues.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;


protected:
  void bindTree_(multidraw::FunctionLibrary&) override;

  std::array<float,11> outputValues;

  UIntValueReader* nGenPart{};
  IntArrayReader* GenPart_status{};
  IntArrayReader* GenPart_pdgId{};
  IntArrayReader* GenPart_genPartIdxMother{};
  FloatArrayReader* GenPart_mass{};
  FloatArrayReader* GenPart_pt{};
  FloatArrayReader* GenPart_eta{};
  FloatArrayReader* GenPart_phi{};
  FloatArrayReader* Lepton_pt{};
};

GenLevelObjects::GenLevelObjects() :
  TTreeFunction(){}

void
GenLevelObjects::beginEvent(long long _iEntry)
{
  setValues();
}


double
GenLevelObjects::evaluate(unsigned iJ)
{
  return outputValues[iJ];
}

void
GenLevelObjects::setValues()
{
  // first of all: if things go bad I want to put zero in all the outputs. I'll have a flag that marks the event as bad.
  for (int i = 1; i <= 10; i++) {
    outputValues[i] = 0.;
  }

  // flag that defines if an event is good or not
  std::cout << "  " << std::endl;
  float FLAG = 0.;

  // searching for indexes (among the Gen Partcles) of the leptons I care about:
  int idxl0 = 0;
  int idxl1 = 0;
  float provl0 = 9999.9;
  float provl1 = 9999.9;
  for (long unsigned int i=0; i< *(nGenPart->Get()); ++i){
    if ((abs(GenPart_pdgId->At(i)) == 11 || abs(GenPart_pdgId->At(i)) == 13 ) && (GenPart_status->At(i) == 1) && (abs(Lepton_pt->At(0) - GenPart_pt->At(i)) < provl0)){
      provl0 = abs(Lepton_pt->At(0) - GenPart_pt->At(i));
      idxl0 = i;
    }
    if ((abs(GenPart_pdgId->At(i)) == 11 || abs(GenPart_pdgId->At(i)) == 13 ) && (GenPart_status->At(i) == 1) && (abs(Lepton_pt->At(1) - GenPart_pt->At(i)) < provl1)){
      provl1 = abs(Lepton_pt->At(1) - GenPart_pt->At(i));
      idxl1 = i;
    }
  }

  // Now I have indexes among the GenParts of the electron and muon, or idx 999 if sth went wrong
  if (idxl0 == 0 || idxl1 == 0){
    std::cout << "Couldn't find the two e/m leptons" << std::endl;
    FLAG = 1.;
  }

  // let's now get the mothers and check if they are W. lep w/ status 1 points at lep w/status 23 which points at W.
  int idxW_l0 = GenPart_genPartIdxMother->At(GenPart_genPartIdxMother->At(idxl0));
  int idxW_l1 = GenPart_genPartIdxMother->At(GenPart_genPartIdxMother->At(idxl1));
  if (abs(GenPart_pdgId->At(idxW_l0)) != 24 || abs(GenPart_pdgId->At(idxW_l1)) != 24) {
    std::cout << "Mother of e/m is not W" << std::endl;
    FLAG = 2.;
  }
  std::cout << "l0 = " << idxW_l0 << "    l1 = " << idxW_l1 << std::endl;

  // Let's find the neutrinos that match my leptons :)
  int idxNeu0 = 99;
  int idxNeu1 = 99;
  for (long unsigned int i=0; i< *(nGenPart->Get()); ++i){
    if ((abs(GenPart_pdgId->At(i)) == 12 || abs(GenPart_pdgId->At(i)) == 14 ) && (GenPart_status->At(i) == 1)){
      int idxmom = GenPart_genPartIdxMother->At(GenPart_genPartIdxMother->At(i));
      std::cout << "indxmom = " << idxmom << std::endl;
      if (idxmom == idxW_l0){
        idxNeu0 = i;
        std::cout << "match 0   idx=" << idxNeu0 << std::endl;
      } else if (idxmom == idxW_l1) {
        idxNeu1 = i;
        std::cout << "match 1   idx=" << idxNeu1 << std::endl;
      } else {
        std::cout << "unmatched" << std::endl;
      }
    }
  }
  // Sometimes I have two good neutrinos and a third unmatched. This case will still be considered good
  // The problem is if I have zero or only one good neutrinos (i.e. the neutrino index is still 99)! Let's check for that
  if ((idxNeu0 == 99) || (idxNeu1 == 99)){
    FLAG = 3;
    idxNeu0 = 0; // put idx to zero, otherwise I'm scared it breaks later. The FLAG tracks the goodness of the outputs
    idxNeu1 = 0;
  }

  outputValues[0] = FLAG;

  outputValues[1] = GenPart_mass->At(idxNeu0);
  outputValues[2] = GenPart_pt->At(idxNeu0);
  outputValues[3] = GenPart_eta->At(idxNeu0);
  outputValues[4] = GenPart_phi->At(idxNeu0);
  outputValues[5] = GenPart_pdgId->At(idxNeu0);

  outputValues[6] = GenPart_mass->At(idxNeu1);
  outputValues[7] = GenPart_pt->At(idxNeu1);
  outputValues[8] = GenPart_eta->At(idxNeu1);
  outputValues[9] = GenPart_phi->At(idxNeu1);
  outputValues[10] = GenPart_pdgId->At(idxNeu1);


  return;
}

void
GenLevelObjects::bindTree_(multidraw::FunctionLibrary& _library)
{
  _library.bindBranch(nGenPart, "nGenPart");
  _library.bindBranch(GenPart_status, "GenPart_status"),
  _library.bindBranch(GenPart_pdgId, "GenPart_pdgId");
  _library.bindBranch(GenPart_genPartIdxMother, "GenPart_genPartIdxMother");
  _library.bindBranch(GenPart_mass, "GenPart_mass");
  _library.bindBranch(GenPart_pt, "GenPart_pt");
  _library.bindBranch(GenPart_eta, "GenPart_eta");
  _library.bindBranch(GenPart_phi, "GenPart_phi");
  _library.bindBranch(Lepton_pt, "Lepton_pt");
}
