 #define Analysis_Dec_cxx
#include "Analysis_Dec.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <vector>
#include <string>

std::vector<Color_t> myColors = {kBlack, kViolet-1, kBlue, kCyan+1, kGreen+1, kOrange-3, kRed};

Double_t enLossMC_0[6] = {3.493, 78.936, 52.756, 42.741, 37.122, 33.631};
Double_t d_enLossMC_0[6] = {0.004, 0.011, 0.011, 0.012, 0.012, 0.013};

Double_t enLossMC_1[6] = {3.689, 83.434, 53.724, 43.176, 37.320, 33.710};
Double_t d_enLossMC_1[6] = {0.004, 0.011, 0.011, 0.012, 0.013, 0.013};

//Double_t enLossMC_2[6] = {3.933, 88.891, 54.754, 43.549, 37.529, 33.874};
//Double_t d_enLossMC_2[6] = {0.004, 0.012, 0.012, 0.012, 0.013, 0.013};
Double_t enLossMC_2[5] = {88.891, 54.754, 43.549, 37.529, 33.874};
Double_t d_enLossMC_2[5] = {0.012, 0.012, 0.012, 0.013, 0.013};

Double_t s_param[7];
Double_t k_param[7];
Double_t k_param_MC[7];




//Funzione generale che ti ho creato io come esempio
void Analysis_Dec::DoAll()
{
  Init_Histograms(); //funzione che inizializza gli istogrammi
  cout << "Ok"<< endl;
  Loop();

  //PlotDeltaBars(_MapDeltaBars10);
  //DeltaBars_vs_beta(_MapDeltaBars10);
  //PlotDeltaBars10();
  //PlotDeltaBars20();
  //PlotDeltaBars21();
  //TimeRes_bar1();
  //TimeRes_bar2();
  //PlotCharge(_EnChargeMap1);
  //PlotCharge_bar3();
  //PlotTimestamp();
  //Charge_vs_Energy(_EnChargeMap0, enLossMC_0, d_enLossMC_0);
  //Charge_vs_Energy(_EnChargeMap1, enLossMC_1, d_enLossMC_1);
  //Charge_vs_Energy_bar3(_EnChargeMap2, enLossMC_2, d_enLossMC_2);
  //LoopDeltaE();
  //EnergyRes_bar3(_EnChargeMap2);

}

void Analysis_Dec::BirksParameters()
{
  Init_Histograms();
  Loop();
  Charge_vs_Energy(_EnChargeMap0, enLossMC_0, d_enLossMC_0, 0);
  Charge_vs_Energy(_EnChargeMap1, enLossMC_1, d_enLossMC_1, 1);
  Charge_vs_Energy_bar3(_EnChargeMap2, enLossMC_2, d_enLossMC_2);
  cout << sMap["a"][1] << endl;

  TMultiGraph* mgS = new TMultiGraph();
  mgS->SetTitle("");
  mgS->GetXaxis()->SetTitle("OverVoltage [V]");
  mgS->GetYaxis()->SetTitle("s");
  TLegend* ls = new TLegend(0.1, 0.8, 0.48, 0.9);

  TMultiGraph* mgK = new TMultiGraph();
  mgK->SetTitle("");
  mgK->GetXaxis()->SetTitle("OverVoltage [V]");
  mgK->GetYaxis()->SetTitle("k [MeV^{-1}]");
  TLegend* lk = new TLegend(0.1, 0.8, 0.48, 0.9);

  TGraphErrors* sgraph0 = new TGraphErrors(7, ovTrue, sMap["a"], nullptr, sMap["da"]);
  sgraph0->SetMarkerStyle(7);
  sgraph0->SetMarkerColor(kBlack);
  sgraph0->SetLineStyle(9);
  sgraph0->SetLineColor(kBlack);
  sgraph0->SetMarkerStyle(20);
  ls->AddEntry(sgraph0, Form("First bar"));
  mgS->Add(sgraph0);

  TGraphErrors* sgraph1 = new TGraphErrors(7, ovTrue, sMap["b"], nullptr, sMap["db"]);
  sgraph1->SetMarkerStyle(7);
  sgraph1->SetMarkerColor(kBlack);
  sgraph1->SetLineStyle(9);
  sgraph1->SetLineColor(kBlue);
  sgraph1->SetMarkerStyle(20);
  ls->AddEntry(sgraph1, Form("Second bar"));
  mgS->Add(sgraph1);

  TGraphErrors* sgraph2 = new TGraphErrors(7, ovTrue, sMap["c"], nullptr, sMap["dc"]);
  sgraph2->SetMarkerStyle(7);
  sgraph2->SetMarkerColor(kBlack);
  sgraph2->SetLineStyle(9);
  sgraph2->SetLineColor(kRed);
  sgraph2->SetMarkerStyle(20);
  ls->AddEntry(sgraph2, Form("Third bar"));
  mgS->Add(sgraph2);


  TGraphErrors* kgraph_0 = new TGraphErrors(7, ovTrue, kMap["a"], nullptr, kMap["da"]);
  kgraph_0->SetMarkerStyle(7);
  kgraph_0->SetMarkerColor(kBlack);
  kgraph_0->SetLineStyle(9);
  kgraph_0->SetLineColor(kBlack);
  kgraph_0->SetMarkerStyle(20);
  lk->AddEntry(kgraph_0, Form("First bar"));
  mgK->Add(kgraph_0);

  TGraphErrors* kgraph_1 = new TGraphErrors(7, ovTrue, kMap["b"], nullptr, kMap["db"]);
  kgraph_1->SetMarkerStyle(7);
  kgraph_1->SetMarkerColor(kBlack);
  kgraph_1->SetLineStyle(9);
  kgraph_1->SetLineColor(kBlue);
  kgraph_1->SetMarkerStyle(20);
  lk->AddEntry(kgraph_1, Form("Second bar"));
  mgK->Add(kgraph_1);

  TGraphErrors* kgraph_2 = new TGraphErrors(7, ovTrue, kMap["c"], nullptr, kMap["dc"]);
  kgraph_2->SetMarkerStyle(7);
  kgraph_2->SetMarkerColor(kBlack);
  kgraph_2->SetLineStyle(9);
  kgraph_2->SetLineColor(kRed);
  kgraph_2->SetMarkerStyle(20);
  lk->AddEntry(kgraph_2, Form("Third bar"));
  mgK->Add(kgraph_2);

  TCanvas* cs = new TCanvas("sparam","sparam",800,600);
  mgS->Draw("aple");
  ls->Draw("same");

  TCanvas* ck = new TCanvas("kparam","kparam",800,600);
  mgK->Draw("aple");
  lk->Draw("same");




  //cout << kMap << endl;
}


/*La funzione Loop() è generata in automatico e carica gli eventi nel tree uno alla volta con la funzione GetEntry():
 serve solitamente per salvare i dati che ti interessano in delle strutture (istogrammi, array, grafici ...) da
 analizzare in seguito: ti metto un esempio*/
void Analysis_Dec::Loop()
{

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;


   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // Qui la funzione GetEntry ti recupera l'evento jentry e salva le quantità corrispondenti nelle variabili della classe
      // definite nel .h, ad esempio BAR_PedB o BAR_TOF_Uncal e così via

      //Qua sotto puoi riempire gli istogrammi (o quello che vuoi) con i dati che ti servono

      _EnChargeMap0[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Charge[0]);
      _EnChargeMap1[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Charge[1]);
      if (!(Tags_BeamEnergy != 60 && BAR_Charge[2] < 20)) _EnChargeMap2[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Charge[2]);



      _MapDeltaBars10[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Timestamp[1] - BAR_Timestamp[0]);
      _MapDeltaBars20[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Timestamp[2] - BAR_Timestamp[0]);
      _MapDeltaBars21[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_Timestamp[2] - BAR_Timestamp[1]);

      _MapEnTOF1[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_TOF_Uncal[0]);
      _MapEnTOF2[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(BAR_TOF_Uncal[1]);


      // if (Cut(ientry) < 0) continue;
   }
}

void Analysis_Dec::LoopDeltaE()
{

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;


   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // Qui la funzione GetEntry ti recupera l'evento jentry e salva le quantità corrispondenti nelle variabili della classe
      // definite nel .h, ad esempio BAR_PedB o BAR_TOF_Uncal e così via

      //Qua sotto puoi riempire gli istogrammi (o quello che vuoi) con i dati che ti servono

      Double_t DeltaE;
      DeltaE = BAR_Charge[0] / (s_param[Tags_OverVoltage-1] - k_param_MC[Tags_OverVoltage-1]*BAR_Charge[0]);
      _DeltaEChargeMap0[Tags_BeamEnergy][Tags_OverVoltage-1]->Fill(DeltaE);


      // if (Cut(ientry) < 0) continue;
   }
}


void Analysis_Dec::Init_Histograms()
{
  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];

    _EnChargeMap0[en] = new TH1D*[7];
    _EnChargeMap1[en] = new TH1D*[7];
    _EnChargeMap2[en] = new TH1D*[7];

    _DeltaEChargeMap0[en] = new TH1D*[7];
    _DeltaEChargeMap1[en] = new TH1D*[7];

    _EnTimestampMap[en] = new TH1D*[7];

    _MapEnTOF1[en] = new TH1D*[7];
    _MapEnTOF2[en] = new TH1D*[7];

    _MapDeltaBars10[en] = new TH1D*[7];
    _MapDeltaBars20[en] = new TH1D*[7];
    _MapDeltaBars21[en] = new TH1D*[7];

    for (Int_t ov=0; ov<7; ov++)
    {
      //if (en == 60) _EnChargeMap0[en][ov] = new TH1D("", "", 300, 0, 8);
      _EnChargeMap0[en][ov] = new TH1D("", "", 400, 0, 80);
      _EnChargeMap1[en][ov] = new TH1D("", "", 400, 0, 80);
      _EnChargeMap2[en][ov] = new TH1D("", "", 250, 0, 250);

      if (en == 60)
      {
        _EnChargeMap0[en][ov] = new TH1D("", "", 800, 0, 80);
        _EnChargeMap1[en][ov] = new TH1D("", "", 800, 0, 80);
        _EnChargeMap2[en][ov] = new TH1D("", "", 150, 0, 40);

        _DeltaEChargeMap0[en][ov] = new TH1D("","", 1000, 0, 50);
        _DeltaEChargeMap1[en][ov] = new TH1D("","", 1000, 0, 50);
      }
      else
      {
        _DeltaEChargeMap0[en][ov] = new TH1D("","", 200, 0, 110);
        _DeltaEChargeMap1[en][ov] = new TH1D("","", 200, 0, 110);
      }

      _EnTimestampMap[en][ov] = new TH1D("", "", 300, 0, 300);

      _MapEnTOF1[en][ov] = new TH1D("","",570, 5, 25);
      _MapEnTOF2[en][ov] = new TH1D("","",570, 5, 25);

      _MapDeltaBars10[en][ov] = new TH1D("","",150, 0.5, 5);
      if (en == 60)
      {
        _MapDeltaBars20[en][ov] = new TH1D("","",150, 1, 6);
        _MapDeltaBars21[en][ov] = new TH1D("","",150, 0, 3);
      }
      else
      {
        _MapDeltaBars20[en][ov] = new TH1D("","",150,0.5,5);
        _MapDeltaBars21[en][ov] = new TH1D("","",150,0.5,5);
      }
    }
  }
}



void Analysis_Dec::PlotDeltaBars(std::map<Int_t, TH1D**> dataMap)
{
  Double_t beta[6] = {0.342, 0.142, 0.182, 0.212, 0.237, 0.260};
  //TCanvas* c1 = new TCanvas("Canvas label","Canvas title",800,600);
  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("TOF vs OverVoltage");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("#mu_{#DeltaBars} [ns]");

  TMultiGraph* mgProton = new TMultiGraph();
  mgProton->SetTitle("Protons Time Resolution vs OverVoltage");
  mgProton->GetXaxis()->SetTitle("OverVoltage [V]");
  mgProton->GetYaxis()->SetTitle("#sigma_{#DeltaBars} [ns]");

  TMultiGraph* Tres = new TMultiGraph();
  TLegend* legend2 = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend2->SetHeader("Legend", "C");
  Tres->SetTitle("Carbon Ions Time Resolution vs OverVoltage");
  Tres->GetXaxis()->SetTitle("OverVoltage [V]");
  Tres->GetYaxis()->SetTitle("#sigma_{#DeltaBars} [ns]");

  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    TF1* fitfunc[7];
    Double_t timeMean[7];
    Double_t timeSigma[7];
    Double_t dMean[7];
    Double_t dSigma[7];

    for (Int_t ov=0; ov<7; ov++)
    {
      TCanvas* c = new TCanvas();
      dataMap[en][ov]->SetTitle(Form("E = %d MeV, OV = %d; #DeltaBars [ns]; Entriees", en, ov+1));
      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[ov] = new TF1("fitfunc_label", "[0]+[1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(0, a, mean, std);
      Double_t xmin, xmax;
      xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
      xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
      dataMap[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);

      timeMean[ov] = fitfunc[ov]->GetParameter(2);
      timeSigma[ov] = fitfunc[ov]->GetParameter(3);
      dMean[ov] = fitfunc[ov]->GetParError(3);
      dSigma[ov] = fitfunc[ov]->GetParError(3);

    }

    TGraphErrors* graph = new TGraphErrors(7, ovTrue, timeMean, nullptr, dMean);
    graph->SetMarkerStyle(7);
    graph->SetMarkerColor(kBlack);
    graph->SetLineStyle(9);
    graph->SetLineWidth(2);
    graph->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60) legend->AddEntry(graph, Form("Protons: %d MeV", en));
    else legend->AddEntry(graph, Form("Carbon Ions: %d MeV", en));
    mg->Add(graph);

    TGraphErrors* gSigma = new TGraphErrors(7, ovTrue, timeSigma, nullptr, dSigma);
    gSigma->SetMarkerStyle(7);
    gSigma->SetMarkerColor(kBlack);
    gSigma->SetLineStyle(9);
    gSigma->SetLineWidth(2);
    gSigma->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60)  mgProton->Add(gSigma);
    else
    {
      legend2->AddEntry(gSigma, Form("Carbon Ions: %d MeV", en));
      Tres->Add(gSigma);
    }
  }

  TCanvas* ctot = new TCanvas("ctot","ctot", 800,600);
  mg->GetXaxis()->SetLimits(0., 10.);
  mg->Draw("aple");
  legend->Draw("same");

  TCanvas* cp = new TCanvas("cp","p", 800,600);
  mgProton->Draw("apl");

  TCanvas* cs = new TCanvas("cs","s", 800,600);
  Tres->Draw("apl");
  legend2->Draw("same");
  //cs->Write("Tres vs OV");
}


void Analysis_Dec::DeltaBars_vs_beta(std::map<Int_t, TH1D**> dataMap)
{
  Double_t beta[6] = {0.342, 0.428, 0.555, 0.622, 0.673, 0.713};
  for (Int_t i=0; i<6; i++)
  {
    beta[i] = 1 / beta[i];
  }
  /*
  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  //mg->SetTitle("");
  mg->GetXaxis()->SetTitle("1 / #beta");
  mg->GetYaxis()->SetTitle("#mu_{#DeltaBars} [ns]"); */

  for (Int_t ov=0; ov<7; ov++)
  {
    TF1* fitfunc[6];
    Double_t timeMean[6];
    Double_t timeErr[6];

    for (Int_t i=0; i<6; i++)
    {
      cout << i << endl;
      Int_t en = _Energies[i];
      TCanvas* c = new TCanvas();
      dataMap[en][ov]->SetTitle(Form("#DeltaBars: E = %d MeV, OV = %d; #DeltaBars [ns]; Entriees", en, ov+1));
      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      dataMap[en][ov]->Draw();

      fitfunc[i] = new TF1("fitfunc_label", "[0]+[1]*TMath::Gaus(x,[2],[3])");
      fitfunc[i]->SetParameters(0, a, mean, std);
      Double_t xmin, xmax;
      xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
      xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
      dataMap[en][ov]->Fit(fitfunc[i],"q","", xmin, xmax);

      timeMean[i] = fitfunc[i]->GetParameter(2);
      timeErr[i] = fitfunc[i]->GetParError(2);
    }

    TCanvas* c = new TCanvas();
    TGraphErrors* graph = new TGraphErrors(6, beta, timeMean, nullptr, timeErr);
    graph->SetTitle("#mu_{#DeltaBars} vs 1/#beta");
    graph->SetMarkerStyle(20);
    graph->SetMarkerSize(0.8);
    graph->SetMarkerColor(kBlack);
    graph->Draw("ape");
    graph->GetXaxis()->SetTitle("1 / #beta");
    graph->GetYaxis()->SetTitle("#mu_{#DeltaBars} [ns]");
    TF1* line = new TF1("", "[0]+x*[1]", 0, 5);
    //;
    //gStyle->SetOptFit(1);
    line->SetLineColor(kRed);
    line->SetLineWidth(2);
    graph->Fit(line);
    line->Draw("same");

    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    //if (en == 60) legend->AddEntry(graph, Form("Protons: %d MeV", en));
    //else legend->AddEntry(graph, Form("Carbon Ions: %d MeV", en));
    //mg->Add(graph);
  }
  //TCanvas* ctot = new TCanvas("ctot","ctot", 800,600);
  //mg->GetXaxis()->SetLimits(0., 10.);
  //mg->Draw("aple");
  //legend->Draw("same");

}


void Analysis_Dec::TimeRes_bar1()
{
  //gStyle->SetOptStat(0);
  TMultiGraph* mg = new TMultiGraph();


  TLegend* legend = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("TOF vs OverVoltage: first bar");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("#mu_{TOF} [ns]");

  TMultiGraph* mgProton = new TMultiGraph();
  mgProton->SetTitle("Protons Time Resolution vs OverVoltage");
  mgProton->GetXaxis()->SetTitle("OverVoltage [V]");
  mgProton->GetYaxis()->SetTitle("#sigma_{#TOF} [ns]");

  TMultiGraph* Tres = new TMultiGraph();
  TLegend* legend2 = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend2->SetHeader("Legend", "C");
  Tres->SetTitle("Time Resolution vs OverVoltage: first bar");
  Tres->GetXaxis()->SetTitle("OverVoltage [V]");
  Tres->GetYaxis()->SetTitle("#sigma_{TOF} [ns]");
  //mg->GetXaxis()->SetLimits(0., 250.);
  TFile* OutFile = new TFile("TimeRes_bar1.root", "RECREATE");

  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    Double_t timeMean[7];
    Double_t timeSigma[7];
    Double_t dMean[7];
    Double_t dSigma[7];
    //TCanvas* c = new TCanvas();
    TF1* fitfunc[7];
    for (Int_t ov=0; ov<7; ov++)
    {
      TCanvas* c = new TCanvas();
      _MapEnTOF1[en][ov]->SetTitle(Form("TOF: E = %d MeV, OV = %d; TOF Value [ns]; Entriees", en, ov+1));
      _MapEnTOF1[en][ov]->Draw("same");
      Double_t a = _MapEnTOF1[en][ov]->GetMaximum();
      Double_t mean = _MapEnTOF1[en][ov]->GetMean();
      Double_t std = _MapEnTOF1[en][ov]->GetStdDev();
      fitfunc[ov] = new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(0, a, mean, std);

      /*
      if (en == 400 && ov+1 == 4) fitfunc[ov]->SetParameters(0, a, 8, 0.02);
      if (en == 330 && ov +1== 5) fitfunc[ov]->SetParameters(0, a, 8.6, 0.02);
      if (en == 330 && ov +1== 2) fitfunc[ov]->SetParameters(0, a, 8.8, 0.02);
      if (en == 190 && ov +1== 5) fitfunc[ov]->SetParameters(600, a, 8, 0.3);

      if (en == 260 && ov +1== 4) fitfunc[ov]->SetParameters(0, a, 10, 0.02);
      if (en == 190 && ov +1== 7) fitfunc[ov]->SetParameters(0, a, 9.4, 0.02);
      if (en == 190 && ov +1== 2) fitfunc[ov]->SetParameters(0, a, 10, 0.02);
      */


      fitfunc[ov]->SetParLimits(1, a-1000, a+1000);
      fitfunc[ov]->SetParLimits(2, 8, 14);
      fitfunc[ov]->SetParLimits(3, 0.01, 0.8);
      gStyle->SetOptFit();
      Double_t xmin, xmax;
      xmin = _MapEnTOF1[en][ov]->GetMean() - 3* _MapEnTOF1[en][ov]->GetStdDev();
      xmax = _MapEnTOF1[en][ov]->GetMean() + 3* _MapEnTOF1[en][ov]->GetStdDev();
      _MapEnTOF1[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);
      fitfunc[ov]->Draw("same");

      cout << fitfunc[ov]->GetParameter(2) << endl;

      timeMean[ov] = fitfunc[ov]->GetParameter(2);
      timeSigma[ov] = fitfunc[ov]->GetParameter(3);
      dMean[ov] = fitfunc[ov]->GetParError(2);
      dSigma[ov] = fitfunc[ov]->GetParError(3);
      _MapEnTOF1[en][ov]->Write(Form("Charges, E = %d MeV, OV = %d", en, ov+1));
    }
    //TCanvas* cc = new TCanvas("","",800,600);
    TGraphErrors* graph = new TGraphErrors(7, ovTrue, timeMean, nullptr, dMean);
    graph->SetMarkerStyle(7);
    graph->SetMarkerColor(kBlack);
    graph->SetLineStyle(9);
    graph->SetLineWidth(2);
    graph->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60) legend->AddEntry(graph, Form("Protons: %d MeV", en));
    else legend->AddEntry(graph, Form("Carbon Ions: %d MeV", en));
    mg->Add(graph);

    TGraphErrors* gSigma = new TGraphErrors(7, ovTrue, timeSigma, nullptr, dSigma);
    gSigma->SetMarkerStyle(7);
    gSigma->SetMarkerColor(kBlack);
    gSigma->SetLineStyle(9);
    gSigma->SetLineWidth(2);
    gSigma->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60)  mgProton->Add(gSigma);
    else
    {
      legend2->AddEntry(gSigma, Form("Carbon Ions: %d MeV", en));
      Tres->Add(gSigma);
    }
  }
  TCanvas* ctot = new TCanvas("ctot","ctot", 800,600);
  mg->GetXaxis()->SetLimits(0., 10.);
  mg->Draw("aple");
  legend->Draw("same");
  ctot->Write("TOF vs OV");

  TCanvas* cs = new TCanvas("cs","s", 800,600);
  Tres->GetXaxis()->SetLimits(0., 10.);
  Tres->Draw("apl");
  legend2->Draw("same");
  cs->Write("Tres vs OV");

  TCanvas* cp = new TCanvas("cp","p", 800,600);
  mgProton->Draw("apl");
  cp->Write("P Tres vs OV");

  OutFile->Close();

}


void Analysis_Dec::TimeRes_bar2()
{
  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("TOF vs OverVoltage: second bar");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("#mu_{TOF} [ns]");

  TMultiGraph* mgProton = new TMultiGraph();
  mgProton->SetTitle("Protons Time Resolution vs OverVoltage");
  mgProton->GetXaxis()->SetTitle("OverVoltage [V]");
  mgProton->GetYaxis()->SetTitle("#sigma_{#TOF} [ns]");

  TMultiGraph* Tres = new TMultiGraph();
  TLegend* legend2 = new TLegend(0.01, 0.7, 0.48, 0.9);
  legend2->SetHeader("Legend", "C");
  Tres->SetTitle("Time Resolution vs OverVoltage: second bar");
  Tres->GetXaxis()->SetTitle("OverVoltage [V]");
  Tres->GetYaxis()->SetTitle("#sigma_{TOF} [ns]");

  TFile* OutFile = new TFile("TimeRes_bar2.root", "RECREATE");

  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    Double_t timeMean[7];
    Double_t timeSigma[7];
    Double_t dMean[7];
    Double_t dSigma[7];
    //TCanvas* c = new TCanvas();
    TF1* fitfunc[7];
    for (Int_t ov=0; ov<7; ov++)
    {
      TCanvas* c = new TCanvas();
      _MapEnTOF2[en][ov]->SetTitle(Form("TOF: E = %d MeV, OV = %d; Charge Value; Entriees", en, ov+1));
      _MapEnTOF2[en][ov]->Draw("same");
      Double_t a = _MapEnTOF2[en][ov]->GetMaximum();
      Double_t mean = _MapEnTOF2[en][ov]->GetMean();
      Double_t std = _MapEnTOF2[en][ov]->GetStdDev();
      fitfunc[ov] = new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(0, a, mean, std);
      /*
      if (en == 400 && ov+1 == 4) fitfunc[ov]->SetParameters(0, a, 9, 0.02);
      if (en == 330 && ov +1== 5) fitfunc[ov]->SetParameters(0, a, 10, 0.02);
      if (en == 330 && ov +1== 2) fitfunc[ov]->SetParameters(0, a, 10, 0.02);
      if (en == 190 && ov +1== 5) fitfunc[ov]->SetParameters(600, a, 10, 0.3);
      */
      if (en == 60 && ov+1 == 1) fitfunc[ov]->SetParameters(0, a, mean, 0.7);


      fitfunc[ov]->SetParLimits(1, a-1000, a+1000);
      fitfunc[ov]->SetParLimits(2, 9, 15);
      fitfunc[ov]->SetParLimits(3, 0.01, 0.8);
      gStyle->SetOptFit();
      Double_t xmin, xmax;
      xmin = _MapEnTOF2[en][ov]->GetMean() - 3* _MapEnTOF2[en][ov]->GetStdDev();
      xmax = _MapEnTOF2[en][ov]->GetMean() + 3* _MapEnTOF2[en][ov]->GetStdDev();
      _MapEnTOF2[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);
      fitfunc[ov]->Draw("same");

      cout << fitfunc[ov]->GetParameter(2) << endl;

      timeMean[ov] = fitfunc[ov]->GetParameter(2);
      timeSigma[ov] = fitfunc[ov]->GetParameter(3);
      dMean[ov] = fitfunc[ov]->GetParError(2);
      dSigma[ov] = fitfunc[ov]->GetParError(3);
      _MapEnTOF2[en][ov]->Write(Form("TOF, E = %d MeV, OV = %d", en, ov+1));
    }

    //TCanvas* cc = new TCanvas("","",800,600);
    TGraphErrors* graph = new TGraphErrors(7, ovTrue, timeMean, nullptr, dMean);
    graph->SetMarkerStyle(7);
    graph->SetMarkerColor(kBlack);
    graph->SetLineStyle(9);
    graph->SetLineWidth(2);
    graph->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60) legend->AddEntry(graph, Form("Protons: %d MeV", en));
    else legend->AddEntry(graph, Form("Carbon Ions: %d MeV", en));
    mg->Add(graph);

    TGraphErrors* gSigma = new TGraphErrors(7, ovTrue, timeSigma, nullptr, dSigma);
    gSigma->SetMarkerStyle(7);
    gSigma->SetMarkerColor(kBlack);
    gSigma->SetLineStyle(9);
    gSigma->SetLineWidth(2);
    gSigma->SetLineColor(myColors[i]);;
    //graph->GetYaxis()->SetRange(0., 250.);
    //graph->Draw("aple");
    if (en == 60)  mgProton->Add(gSigma);
    else
    {
      legend2->AddEntry(gSigma, Form("Carbon Ions: %d MeV", en));
      Tres->Add(gSigma);
    }
  }
  TCanvas* ctot = new TCanvas("ctot","ctot", 800,600);
  mg->GetXaxis()->SetLimits(0., 10.);
  mg->Draw("aple");
  legend->Draw("same");
  ctot->Write("TOF vs OV");

  TCanvas* cs = new TCanvas("cs","s", 800,600);
  Tres->GetXaxis()->SetLimits(0., 10.);
  Tres->Draw("apl");
  legend2->Draw("same");
  cs->Write("C Tres vs OV");

  TCanvas* cp = new TCanvas("cp","p", 800,600);
  mgProton->Draw("apl");
  cp->Write("P Tres vs OV");

  OutFile->Close();
}


void Analysis_Dec::PlotCharge(std::map<Int_t, TH1D**> dataMap)
{
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("Global charge vs OV: second bar");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("Charge");

  //TFile* OutFile = new TFile("Charge_bar2.root", "RECREATE");

  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    TF1* fitfunc[7];
    Double_t charge[7];
    Double_t d_charge[7];
    TCanvas* c2 = new TCanvas();

    for (Int_t ov=0; ov<7; ov++)
    {
      dataMap[en][ov]->SetTitle(Form("Charges: E = %d MeV, OV = %d; Charge Value; Entriees", en, ov+1));
      dataMap[en][ov]->Draw("same");
      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[ov]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      if (en == 60 && ov ==0)
      {
        fitfunc[ov]->SetParameters(0, 5000, 1, 0.1);
        //fitfunc[ov]->SetParLimits(2, 0.8, 1.2);
        dataMap[en][ov]->Fit(fitfunc[ov],nullptr,nullptr,0,2);
      }
      else
      {
        fitfunc[ov]->SetParameters(1, a, mean, std);
        Double_t xmin, xmax;
        xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
        xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
        dataMap[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);
        fitfunc[ov]->Draw("same");
      }
      charge[ov] = fitfunc[ov]->GetParameter(2);
      d_charge[ov] = fitfunc[ov]->GetParError(2);
      //dataMap[en][ov]->Write(Form("Charges, E = %d MeV, OV = %d", en, ov+1));
    }

    TGraphErrors* graph = new TGraphErrors(7, ovTrue, charge, nullptr, d_charge);
    graph->SetMarkerStyle(kOpenCircle);
    graph->SetMarkerColor(kBlack);
    graph->SetLineColor(kBlack);
    //graph->SetTitle(Form("%d", en));
    //graph->Draw("APE");

    //Fitting a function to previous data
    TF1* line = new TF1("", "[0]+x*[1]+[2]*x*x", 0, 10.5);

    line->SetLineColor(myColors[i]);;
    graph->Fit(line);
    if (en == 60) legend->AddEntry(line, Form("Protons: %d MeV", en));
    else legend->AddEntry(line, Form("Carbon Ions: %d MeV", en));
    mg->Add(graph);
  }
  TCanvas* ctot = new TCanvas("ctot","ctot",800,600);
  mg->Draw("ape");
  legend->Draw("same");
  //ctot->Write("Charge vs OV");
  //OutFile->Close();
}


void Analysis_Dec::PlotCharge_bar3()
{
 gStyle->SetOptStat(0);
 gStyle->SetOptFit(0);

 TMultiGraph* mg = new TMultiGraph();

 TLegend* legend = new TLegend(0.1, 0.7, 0.48, 0.9);
 legend->SetHeader("Legend", "C");
 mg->SetTitle("Global charge vs OV: third bar");
 mg->GetXaxis()->SetTitle("OverVoltage [V]");
 mg->GetYaxis()->SetTitle("Charge");



 for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    Double_t charge[7];
    Double_t d_charge[7];
    TF1* fitfunc[7];



    for (Int_t ov=0; ov<7; ov++)
    {
      TCanvas* c = new TCanvas();
      _EnChargeMap2[en][ov]->Draw("same");
      _EnChargeMap2[en][ov]->SetTitle(Form("Charges: E = %d MeV, OV = %d; Charge Value; Entriees", en, ov+1));
      _EnChargeMap2[en][ov]->Draw("same");
      Double_t a = _EnChargeMap2[en][ov]->GetMaximum();
      Double_t mean = _EnChargeMap2[en][ov]->GetMean();
      Double_t std = _EnChargeMap2[en][ov]->GetStdDev();
      fitfunc[ov]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(0, a, mean, std);
      Double_t xmin, xmax;
      if (en ==60) cout << mean << endl;
      xmin = _EnChargeMap2[en][ov]->GetMean() - 3* _EnChargeMap2[en][ov]->GetStdDev();
      xmax = _EnChargeMap2[en][ov]->GetMean() + 3* _EnChargeMap2[en][ov]->GetStdDev();
      _EnChargeMap2[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);
      fitfunc[ov]->Draw("same");

      charge[ov] = fitfunc[ov]->GetParameter(2);
      d_charge[ov] = fitfunc[ov]->GetParError(2);
    }
    TGraphErrors* graph = new TGraphErrors(7, ovTrue, charge, nullptr, d_charge);
    graph->SetMarkerStyle(kOpenCircle);
    graph->SetMarkerColor(kBlack);
    graph->SetLineColor(kBlack);
    //graph->SetTitle(Form("%d", en));
    //graph->Draw("APE");

    //Fitting a function to previous data
    TF1* line = new TF1("", "[0]+x*[1]+[2]*x*x", 0, 10.5);

    line->SetLineColor(myColors[i]);;
    graph->Fit(line);
    if (en == 60) legend->AddEntry(line, Form("Protons: %d MeV", en));
    else legend->AddEntry(line, Form("Carbon Ions: %d MeV", en));
    mg->Add(graph);
  }
  TCanvas* ctot = new TCanvas("ctot","ctot",800,600);
  mg->Draw("ape");
  legend->Draw("same");
}



void Analysis_Dec::Charge_vs_Energy(std::map<Int_t, TH1D**> dataMap, Double_t* de_MC, Double_t* d_de_MC, Int_t idBar)
{
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  Double_t enLoss[6] = {10.73, 6.534, 4.61, 3.79, 3.315, 3.006};
  Double_t thickness = 0.3;

  Double_t dk[7];

  for (Int_t i=0; i<6; i++)
  {
    if (i > 0) enLoss[i] = 6*6*enLoss[i];
    enLoss[i] = 1.023*thickness*enLoss[i];
  }

  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.1, 0.7, 0.45, 0.9);
  //legend->SetHeader("Legend", "C");



  TMultiGraph* mgMC = new TMultiGraph();
  mgMC->SetTitle("Global charge vs energy loss (MC):");
  mgMC->GetXaxis()->SetTitle("#DeltaE_{MC} [MeV]");
  mgMC->GetYaxis()->SetTitle("Charge");

  //TFile* OutFile = new TFile("Charge_vs_Energy_bar2.root", "RECREATE");

  for (Int_t ov=0; ov<7; ov++)
  {
    TF1* fitfunc[6];
    Double_t charge[6];
    Double_t d_charge[6];


    for (Int_t i=0; i<6; i++)
    {
      Int_t en = _Energies[i];

      TCanvas* c = new TCanvas();
      gStyle->SetOptStat(1);
      dataMap[en][ov]->SetTitle(Form("E = %d MeV, OV = %d; #DeltaE [MeV]; Entriees", en, ov+1));

      dataMap[en][ov]->Draw("same");

      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[i]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      if (en == 60 && ov ==0)
      {
        fitfunc[i]->SetParameters(0, 7000, 1, 0.1);
        dataMap[en][ov]->Fit(fitfunc[ov],nullptr,nullptr,0,2);
      }
      else
      {
        fitfunc[i]->SetParameters(1, a, mean, std);
        Double_t xmin, xmax;
        xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
        xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
        dataMap[en][ov]->Fit(fitfunc[i],"q","", xmin, xmax);
        fitfunc[i]->Draw("same");
      }
      //if (en == 115 && ov == 4) fitfunc[ov]->SetParameters(0, a, 34, 0.9);

      fitfunc[i]->Draw("same");
      charge[i] = fitfunc[i]->GetParameter(2);
      d_charge[i] = fitfunc[i]->GetParError(2);
      //dataMap[en][ov]->Write(Form("Charges, E = %d MeV, OV = %d", en, ov+1));

    }
    //c->Write(Form("Charges, OV = %d", ov+1));

    TGraphErrors* graph = new TGraphErrors(6, enLoss, charge, nullptr, d_charge);
    graph->SetMarkerStyle(24);
    //graph->SetMarkerSize(1);
    graph->SetMarkerColor(kBlack);
    graph->SetLineColor(kBlack);
    TF1* line = new TF1("", "[0]*x / (1 + [1]*x)", 0, 35);

    line->SetLineColor(myColors[ov]);
    graph->Fit(line);
    //s_param[ov] = line->GetParameter(0);
    k_param[ov] = line->GetParameter(1);
    dk[ov] = line->GetParError(1);
    legend->AddEntry(line, Form("OverVoltage: %1.1f V", ovTrue[ov]));
    mg->Add(graph);

    TGraphErrors* graphMC = new TGraphErrors(6, de_MC, charge, d_de_MC, d_charge);
    graphMC->SetMarkerStyle(24);
    //graph->SetMarkerSize(1);
    graphMC->SetMarkerColor(kBlack);
    graphMC->SetLineColor(kBlack);
    graphMC->SetMinimum(0.);
    graphMC->SetMaximum(250.);
    //TF1* line = new TF1("", "[0]*(x / (1 + [1]*x))", 0, 35);
    line->SetLineColor(myColors[ov]);
    graphMC->Fit(line);

    cout << "Fin qui ci arrivo"<< endl;

    if (idBar == 0)
    {
      sMap["a"][ov] = line->GetParameter(0);
      kMap["a"][ov] = line->GetParameter(1);
      sMap["da"][ov] = line->GetParError(0);
      kMap["da"][ov] = line->GetParError(1);
    }
    if (idBar == 1)
    {
      sMap["b"][ov] = line->GetParameter(0);
      kMap["b"][ov] = line->GetParameter(1);
      sMap["db"][ov] = line->GetParError(0);
      kMap["db"][ov] = line->GetParError(1);
    }
    //legend->AddEntry(line, Form("OverVoltage: %d V", ov+1));
    mgMC->Add(graphMC);

  }
  TCanvas* ctot = new TCanvas("nominal","nominal",800,600);
  mg->Draw("ape");
  legend->Draw("same");
  //ctot->Write("Charge vs Energy Loss");
  mg->SetTitle("Global charge vs energy loss");
  mg->GetXaxis()->SetTitle("#DeltaE [MeV]");
  mg->GetYaxis()->SetTitle("Charge");
  //gPad->Modified();
  //mg->GetXaxis()->SetLimits(0., 90.);
  //mg->SetMinimum(0.);
  //mg->SetMaximum(250.);

  TCanvas* cmc = new TCanvas("mc","mc",800,600);
  mgMC->Draw("ape");
  legend->Draw("same");
  //cmc->Write("Charge vs Energy Loss (MC)");
  /*
  TCanvas* ck = new TCanvas("kparam","kparam",800,600);

  TMultiGraph* mk = new TMultiGraph();
  TLegend* lk = new TLegend(0.1, 0.8, 0.48, 0.9);
  //lk->SetHeader("Legend", "C");

  TGraphErrors* kgraph = new TGraphErrors(7, ovTrue, k_param, nullptr, dk);
  kgraph->SetMarkerStyle(7);
  kgraph->SetMarkerColor(kBlack);
  kgraph->SetLineStyle(9);
  kgraph->SetLineColor(kRed);
  kgraph->SetMarkerStyle(20);
  lk->AddEntry(kgraph, Form("k using NIST data"));
  mk->Add(kgraph);

  TGraphErrors* kgraphMC = new TGraphErrors(7, ovTrue, k_param_MC, nullptr, dk_MC);
  kgraphMC->SetMarkerStyle(7);
  kgraphMC->SetMarkerColor(kBlack);
  kgraphMC->SetLineStyle(9);
  kgraphMC->SetLineColor(kBlue);
  kgraphMC->SetMarkerStyle(20);
  lk->AddEntry(kgraphMC, Form("k using MC data"));
  mk->Add(kgraphMC);

  mk->SetTitle("Plot of k parameter: second bar");
  mk->GetXaxis()->SetTitle("OverVoltage [V]");
  mk->GetXaxis()->SetLimits(1., 5.);
  mk->GetYaxis()->SetTitle("k [MeV^{-1}]");
  mk->SetMaximum(0.013);
  mk->SetMinimum(0.009);
  mk->Draw("aple");
  lk->Draw("same");
  //ck->Write("k Plot");
  //OutFile->Close();
  */
}


void Analysis_Dec::Charge_vs_Energy_bar3(std::map<Int_t, TH1D**> dataMap, Double_t* de_MC, Double_t* d_de_MC)
{
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);

  //Double_t enLoss[6] = {10.73, 6.534, 4.61, 3.79, 3.315, 3.006};
  Double_t enLoss[5] = {6.534, 4.61, 3.79, 3.315, 3.006};
  Double_t thickness = 0.3;

  Double_t dk[7];
  Double_t dk_MC[7];


  for (Int_t i=0; i<5; i++)
  {
    enLoss[i] = 6*6*enLoss[i];
    enLoss[i] = 1.023*thickness*enLoss[i];
  }

  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.1, 0.7, 0.48, 0.9);
  //legend->SetHeader("Legend", "C");


  TMultiGraph* mgMC = new TMultiGraph();
  mgMC->SetTitle("Global charge vs energy loss (MC):");
  mgMC->GetXaxis()->SetTitle("#DeltaE_{MC} [MeV]");
  mgMC->GetXaxis()->SetLimits(0., 90.);
  mgMC->GetYaxis()->SetTitle("Charge");

  //TFile* OutFile = new TFile("Charge_vs_Energy_bar2.root", "RECREATE");

  for (Int_t ov=0; ov<7; ov++)
  {
    //TF1* fitfunc[6];
    //Double_t charge[6];
    //Double_t d_charge[6];
    TF1* fitfunc[5];
    Double_t charge[5];
    Double_t d_charge[5];


    for (Int_t i=1; i<6; i++)
    {
      Int_t en = _Energies[i];
      cout << en<< endl;

      TCanvas* c = new TCanvas();
      gStyle->SetOptStat(1);
      dataMap[en][ov]->SetTitle(Form("E = %d MeV, OV = %d; #DeltaE [MeV]; Entriees", en, ov+1));

      dataMap[en][ov]->Draw("same");

      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[i-1]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      if (en == 60 && ov ==0)
      {
        fitfunc[i-1]->SetParameters(0, 7000, 1, 0.1);
        dataMap[en][ov]->Fit(fitfunc[i-1],nullptr,nullptr,0,2);
      }
      else
      {
        fitfunc[i-1]->SetParameters(1, a, mean, std);
        Double_t xmin, xmax;
        xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
        xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
        dataMap[en][ov]->Fit(fitfunc[i-1],"q","", xmin, xmax);
        fitfunc[i-1]->Draw("same");
      }
      //if (en == 115 && ov == 4) fitfunc[ov]->SetParameters(0, a, 34, 0.9);

      fitfunc[i-1]->Draw("same");
      charge[i-1] = fitfunc[i-1]->GetParameter(2);
      d_charge[i-1] = fitfunc[i-1]->GetParError(2);
      //dataMap[en][ov]->Write(Form("Charges, E = %d MeV, OV = %d", en, ov+1));

    }
    //c->Write(Form("Charges, OV = %d", ov+1));

    TGraphErrors* graph = new TGraphErrors(5, enLoss, charge, nullptr, d_charge);
    graph->SetMarkerStyle(24);
    //graph->SetMarkerSize(1);
    graph->SetMarkerColor(kBlack);
    graph->SetLineColor(kBlack);
    TF1* line = new TF1("", "[0]*x / (1 + [1]*x)", 0, 90);
    ;
    line->SetLineColor(myColors[ov]);
    graph->Fit(line);
    //s_param[ov] = line->GetParameter(0);
    sMap["c"][ov] = line->GetParameter(0);
    kMap["c"][ov] = line->GetParameter(1);
    sMap["dc"][ov] = line->GetParError(0);
    kMap["dc"][ov] = line->GetParError(1);
    legend->AddEntry(line, Form("OverVoltage: %1.1f V", ovTrue[ov]));
    mg->Add(graph);

    TGraphErrors* graphMC = new TGraphErrors(5, de_MC, charge, d_de_MC, d_charge);
    graphMC->SetMarkerStyle(24);
    graphMC->GetXaxis()->SetLimits(0., 90.);
    //graph->SetMarkerSize(1);
    graphMC->SetMarkerColor(kBlack);
    graphMC->SetLineColor(kBlack);
    //TF1* line = new TF1("", "[0]*(x / (1 + [1]*x))", 0, 35);
    line->SetLineColor(myColors[ov]);
    graphMC->Fit(line);

    s_param[ov] = line->GetParameter(0);
    k_param_MC[ov] = line->GetParameter(1);
    dk_MC[ov] = line->GetParError(1);
    //legend->AddEntry(line, Form("OverVoltage: %d V", ov+1));
    mgMC->Add(graphMC);

  }
  TCanvas* ctot = new TCanvas("nominal","nominal",800,600);
  mg->SetTitle("Global charge vs energy loss");
  mg->GetXaxis()->SetTitle("#DeltaE [MeV]");
  mg->GetXaxis()->SetLimits(0, 90);
  mg->GetYaxis()->SetTitle("Charge");
  mg->SetMinimum(0.);
  mg->SetMaximum(240.);
  mg->Draw("ape");
  legend->Draw("same");
  //ctot->Write("Charge vs Energy Loss");

  TCanvas* cmc = new TCanvas("mc","mc",800,600);
  mgMC->GetXaxis()->SetLimits(0, 90);
  mgMC->GetYaxis()->SetTitle("Charge");
  mgMC->SetMinimum(0.);
  mgMC->SetMaximum(240.);
  mgMC->Draw("ape");
  legend->Draw("same");
  //cmc->Write("Charge vs Energy Loss (MC)");
  /*
  TCanvas* ck = new TCanvas("kparam","kparam",800,600);

  TMultiGraph* mk = new TMultiGraph();
  TLegend* lk = new TLegend(0.1, 0.7, 0.48, 0.9);
  //lk->SetHeader("Legend", "C");
  mk->SetTitle("Plot of k parameter: third bar");
  mk->GetXaxis()->SetTitle("OverVoltage [V]");
  mk->GetYaxis()->SetTitle("k [MeV^{-1}]");

  TGraphErrors* kgraph = new TGraphErrors(7, ovTrue, k_param, nullptr, dk);
  kgraph->SetMarkerStyle(7);
  kgraph->SetMarkerColor(kBlack);
  kgraph->SetLineStyle(9);
  kgraph->SetLineColor(kRed);
  kgraph->SetMarkerStyle(20);
  lk->AddEntry(kgraph, Form("k using NIST data"));
  mk->Add(kgraph);

  TGraphErrors* kgraphMC = new TGraphErrors(7, ovTrue, k_param_MC, nullptr, dk_MC);
  kgraphMC->SetMarkerStyle(7);
  kgraphMC->SetMarkerColor(kBlack);
  kgraphMC->SetLineStyle(9);
  kgraphMC->SetLineColor(kBlue);
  kgraphMC->SetMarkerStyle(20);
  lk->AddEntry(kgraphMC, Form("k using MC data"));
  mk->Add(kgraphMC);

  mk->Draw("aple");
  lk->Draw("same");
  //ck->Write("k Plot");
  //OutFile->Close();
  */
}


void Analysis_Dec::EnergyRes(std::map<Int_t, TH1D**> dataMap)
{
  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.9, 0.7, 0.6, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("Energy Resolution vs OverVoltage");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("#sigma_{#DeltaE}/#mu_{#DeltaE}");

  for (Int_t i=0; i<6; i++)
  {
    Int_t en = _Energies[i];
    TF1* fitfunc[7];
    Double_t ESigma[7];
    Double_t dSigma[7];

    for (Int_t ov=0; ov<7; ov++)
    {
      gStyle->SetOptStat(1);
      TCanvas* c = new TCanvas();
      dataMap[en][ov]->SetTitle(Form("#DeltaE: E = %d MeV, OV = %d; #DeltaE [MeV]; Entriees", en, ov+1));
      dataMap[en][ov]->Draw();
      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[ov]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(1, a, mean, std);
      fitfunc[ov]->SetParLimits(3, 0.1, 6);
      Double_t xmin, xmax;
      xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
      xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
      dataMap[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);

      ESigma[ov] = fitfunc[ov]->GetParameter(3) / fitfunc[ov]->GetParameter(2);
      cout <<"Valor simga: "<< fitfunc[ov]->GetParameter(3) << endl;
      dSigma[ov] = fitfunc[ov]->GetParError(3) / fitfunc[ov]->GetParameter(3);
      dSigma[ov] += fitfunc[ov]->GetParError(2) / fitfunc[ov]->GetParameter(2);
      dSigma[ov] *= ESigma[ov];

      fitfunc[ov]->Draw("same");
    }


    TGraphErrors* gSigma = new TGraphErrors(7, ovTrue, ESigma, nullptr, dSigma);
    gSigma->SetMarkerStyle(7);
    gSigma->SetMarkerColor(kBlack);
    gSigma->SetLineStyle(9);
    gSigma->SetLineWidth(2);
    gSigma->SetLineColor(myColors[i]);
    legend->AddEntry(gSigma, Form("Energy: %d MeV", en));
    mg->Add(gSigma);
  }
  TCanvas* ctot = new TCanvas("e_res","e_res", 800,600);
  mg->Draw("aple");
  legend->Draw("same");
}


void Analysis_Dec::EnergyRes_bar3(std::map<Int_t, TH1D**> dataMap)
{
  TMultiGraph* mg = new TMultiGraph();

  TLegend* legend = new TLegend(0.9, 0.7, 0.6, 0.9);
  legend->SetHeader("Legend", "C");
  mg->SetTitle("Energy Resolution vs OverVoltage");
  mg->GetXaxis()->SetTitle("OverVoltage [V]");
  mg->GetYaxis()->SetTitle("#sigma_{#DeltaE}/#mu_{#DeltaE}");

  for (Int_t i=1; i<6; i++)
  {
    Int_t en = _Energies[i];
    TF1* fitfunc[7];
    Double_t ESigma[7];
    Double_t dSigma[7];

    for (Int_t ov=0; ov<7; ov++)
    {
      gStyle->SetOptStat(1);
      TCanvas* c = new TCanvas();
      dataMap[en][ov]->SetTitle(Form("#DeltaE: E = %d MeV, OV = %f; #DeltaE [MeV]; Entriees", en, ovTrue[ov]));
      dataMap[en][ov]->Draw();
      Double_t a = dataMap[en][ov]->GetMaximum();
      Double_t mean = dataMap[en][ov]->GetMean();
      Double_t std = dataMap[en][ov]->GetStdDev();
      fitfunc[ov]=new TF1("fitfunc_label", "[0] + [1]*TMath::Gaus(x,[2],[3])");
      fitfunc[ov]->SetParameters(1, a, mean, std);
      fitfunc[ov]->SetParLimits(3, 0.1, 6);
      Double_t xmin, xmax;
      xmin = dataMap[en][ov]->GetMean() - 3* dataMap[en][ov]->GetStdDev();
      xmax = dataMap[en][ov]->GetMean() + 3* dataMap[en][ov]->GetStdDev();
      dataMap[en][ov]->Fit(fitfunc[ov],"q","", xmin, xmax);

      ESigma[ov] = fitfunc[ov]->GetParameter(3) / fitfunc[ov]->GetParameter(2);
      cout <<"Valor simga: "<< fitfunc[ov]->GetParameter(3) << endl;
      dSigma[ov] = fitfunc[ov]->GetParError(3) / fitfunc[ov]->GetParameter(3);
      dSigma[ov] += fitfunc[ov]->GetParError(2) / fitfunc[ov]->GetParameter(2);
      dSigma[ov] *= ESigma[ov];

      fitfunc[ov]->Draw("same");
    }
    ;

    TGraphErrors* gSigma = new TGraphErrors(7, ovTrue, ESigma, nullptr, dSigma);
    gSigma->SetMarkerStyle(7);
    gSigma->SetMarkerColor(kBlack);
    gSigma->SetLineStyle(9);
    gSigma->SetLineWidth(2);
    gSigma->SetLineColor(myColors[i]);
    legend->AddEntry(gSigma, Form("Energy: %d MeV", en));
    mg->Add(gSigma);
  }
  TCanvas* ctot = new TCanvas("e_res","e_res", 800,600);
  mg->Draw("aple");
  legend->Draw("same");
}
