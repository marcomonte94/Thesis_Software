//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue May 12 16:25:06 2020 by ROOT version 6.20/00
// from TTree rec_tree/rec_tree
// found on file: try.root
//////////////////////////////////////////////////////////

#ifndef Analysis_Dec_h
#define Analysis_Dec_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <map>

// Header file for the classes stored in the TTree if any.

class Analysis_Dec {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Double_t        STC_Timestamp;
   Double_t        BAR_PedT[3];
   Double_t        BAR_PedB[3];
   Double_t        BAR_AmpT[3];
   Double_t        BAR_AmpB[3];
   Double_t        BAR_ChargeT[3];
   Double_t        BAR_ChargeB[3];
   Double_t        BAR_TimeT[3];
   Double_t        BAR_TimeB[3];
   Double_t        BAR_Charge[3];
   Double_t        BAR_Timestamp[3];
   Double_t        BAR_DeltaT_TB[3];
   Double_t        BAR_LogCratio_TB[3];
   Double_t        BAR_TOF_Uncal[3];
   Double_t        Tags_Gain;
   Double_t        Tags_BeamEnergy;
   Double_t        Tags_PosX;
   Double_t        Tags_PosY;
   Int_t           Tags_PrimaryParticle;
   Int_t           Tags_OverVoltage;

   // List of branches
   TBranch        *b_STC_Timestamp;   //!
   TBranch        *b_BAR_PedT;   //!
   TBranch        *b_BAR_PedB;   //!
   TBranch        *b_BAR_AmpT;   //!
   TBranch        *b_BAR_AmpB;   //!
   TBranch        *b_BAR_ChargeT;   //!
   TBranch        *b_BAR_ChargeB;   //!
   TBranch        *b_BAR_TimeT;   //!
   TBranch        *b_BAR_TimeB;   //!
   TBranch        *b_BAR_Charge;   //!
   TBranch        *b_BAR_Timestamp;   //!
   TBranch        *b_BAR_DeltaT_TB;   //!
   TBranch        *b_BAR_LogCratio_TB;   //!
   TBranch        *b_BAR_TOF_Uncal;   //!
   TBranch        *b_Tags;   //!

   /*Usa questo spazio per definire ogni altra variabile globale della classe che ti può servire per l'analisi
     Di solito le variabili proprie della classe si indicano con un '_' all'inizio*/
   TH1D* _DeltaBars10;
   TH1D* _Charge[7];

   Double_t _Energies[6] = {60, 115, 190, 260, 330, 400};
   Double_t _OV[7] = {1, 2, 3, 4, 5, 6, 7};
   Double_t ovTrue[7] = {1.5, 2, 2.5, 3, 3.5, 4, 4.5};

   std::map<string, Double_t[7]> sMap;
   std::map<string, Double_t[7]> kMap;

   std::map<Int_t, TH1D**> _EnChargeMap0;
   std::map<Int_t, TH1D**> _EnChargeMap1;
   std::map<Int_t, TH1D**> _EnChargeMap2;

   std::map<Int_t, TH1D**> _DeltaEChargeMap0;
   std::map<Int_t, TH1D**> _DeltaEChargeMap1;

   std::map<Int_t, TH1D**> _EnTimestampMap;

   std::map<Int_t, TH1D**> _MapDeltaBars10;
   std::map<Int_t, TH1D**> _MapDeltaBars20;
   std::map<Int_t, TH1D**> _MapDeltaBars21;

   std::map<Int_t, TH1D**> _MapEnTOF1;
   std::map<Int_t, TH1D**> _MapEnTOF2;


   Analysis_Dec(TTree *tree=0);
   virtual ~Analysis_Dec();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   //Qua puoi mettere le dichiarazioni delle tue funzioni
   virtual void     DoAll();
   virtual void     BirksParameters();
   virtual void     LoopDeltaE();
   virtual void     PlotDeltaBars(std::map<Int_t, TH1D**> dataMap);
   virtual void     DeltaBars_vs_beta(std::map<Int_t, TH1D**> dataMap);
   virtual void     PlotCharge(std::map<Int_t, TH1D**> dataMap);
   virtual void     Init_Histograms();
   virtual void     PlotCharge_bar3();
   //virtual void     PlotTimestamp();
   virtual void     Charge_vs_Energy(std::map<Int_t, TH1D**> dataMap, Double_t* de_MC, Double_t* d_de_MC, Int_t idBar);
   virtual void     Charge_vs_Energy_bar3(std::map<Int_t, TH1D**> dataMap, Double_t* de_MC, Double_t* d_de_MC);
   virtual void     TimeRes_bar1();
   virtual void     TimeRes_bar2();
   virtual void     EnergyRes(std::map<Int_t, TH1D**> dataMap);
   virtual void     EnergyRes_bar3(std::map<Int_t, TH1D**> dataMap);
};

#endif

#ifdef Analysis_Dec_cxx
Analysis_Dec::Analysis_Dec(TTree *tree) : fChain(0)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("all_data.root"); //CAMBIA IL NOME DEL FILE CON QUELLO CHE VUOI ANALIZZARE!!!
      if (!f || !f->IsOpen()) {
         f = new TFile("all_data.root");  // ANCHE QUI!!   ->  Per il momento fai delle prove con un file *.rec.root
                                     // poi lo modifichiamo per funzionare su tutti
      }
      f->GetObject("rec_tree",tree);

   }
   Init(tree);
}

Analysis_Dec::~Analysis_Dec()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t Analysis_Dec::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t Analysis_Dec::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void Analysis_Dec::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("STC_Timestamp", &STC_Timestamp, &b_STC_Timestamp);
   fChain->SetBranchAddress("BAR_PedT", BAR_PedT, &b_BAR_PedT);
   fChain->SetBranchAddress("BAR_PedB", BAR_PedB, &b_BAR_PedB);
   fChain->SetBranchAddress("BAR_AmpT", BAR_AmpT, &b_BAR_AmpT);
   fChain->SetBranchAddress("BAR_AmpB", BAR_AmpB, &b_BAR_AmpB);
   fChain->SetBranchAddress("BAR_ChargeT", BAR_ChargeT, &b_BAR_ChargeT);
   fChain->SetBranchAddress("BAR_ChargeB", BAR_ChargeB, &b_BAR_ChargeB);
   fChain->SetBranchAddress("BAR_TimeT", BAR_TimeT, &b_BAR_TimeT);
   fChain->SetBranchAddress("BAR_TimeB", BAR_TimeB, &b_BAR_TimeB);
   fChain->SetBranchAddress("BAR_Charge", BAR_Charge, &b_BAR_Charge);
   fChain->SetBranchAddress("BAR_Timestamp", BAR_Timestamp, &b_BAR_Timestamp);
   fChain->SetBranchAddress("BAR_DeltaT_TB", BAR_DeltaT_TB, &b_BAR_DeltaT_TB);
   fChain->SetBranchAddress("BAR_LogCratio_TB", BAR_LogCratio_TB, &b_BAR_LogCratio_TB);
   fChain->SetBranchAddress("BAR_TOF_Uncal", BAR_TOF_Uncal, &b_BAR_TOF_Uncal);
   fChain->SetBranchAddress("Tags", &Tags_Gain, &b_Tags);
   Notify();
}

Bool_t Analysis_Dec::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void Analysis_Dec::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t Analysis_Dec::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef Analysis_Dec_cxx
