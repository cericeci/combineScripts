#import "TString.h"
#import "TFile.h"
#import "TH2D.h"
#import "TCanvas.h"
#import "TMath.h"
#import <iostream>
void drawPlot(TString rootfile, TString name, TString output){
    TFile* f = new TFile(rootfile, "READ");
    TH2D* theFig = (TH2D*) f->Get(name);
    TH2D* theFig0 = (TH2D*) theFig->Clone();
    for (int i = 1; i < theFig->GetNbinsX()+1; i++){
        //std::cout << i << std::endl;
        for (int j = 1; j < theFig->GetNbinsY()+1; j++){
            //std::cout << i << "," << j << std::endl;
            theFig->SetBinContent(i,j, theFig->GetBinContent(i,j)/TMath::Power(theFig0->GetBinContent(i,i)*theFig0->GetBinContent(j,j), 0.5));    
        }
    }

    TCanvas* c1 = new TCanvas("c","c", 620,480);
    //c1->SetLogz(true);
    theFig->Draw("colz");
    gStyle->SetOptStat(0);
    c1->SaveAs(output);
    f->Close();
}
