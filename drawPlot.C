#import "TString.h"
#import "TFile.h"
#import "TH2D.h"
#import "TCanvas.h"

void drawPlot(TString rootfile, TString name, TString output){
    TFile* f = new TFile(rootfile, "READ");
    TH2D* theFig = (TH2D*) f->Get(name);
    TH2D* theFig0 = (TH2D*) theFig->Clone();
    TCanvas* c1 = new TCanvas("c","c", 620,480);
    theFig->Draw("text colz");
    gStyle->SetOptStat(0);
    c1->SaveAs(output);
    f->Close();
}
