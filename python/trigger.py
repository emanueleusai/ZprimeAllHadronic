from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,kBlack,kWhite
from sys import argv
from os import system

from utils import compare,hadd,doeff,make_plot
gROOT.SetBatch()


path_base='/nfs/dust/cms/user/usaiem/spring15/uhh2.AnalysisModuleRunner.'
data_filename='DATA.DATA_SingleMuon_Run2015D.root'
mc_filename='MC.TTbar.root'

data_file=TFile(path_base+data_filename)
mc_file=TFile(path_base+mc_filename)
outfile=TFile('outfile.root','RECREATE')

# colors=[kRed,kBlue,kBlack,kGreen,kOrange,6,9]

# histo_list=['HT']#,'pT4','SumOfTopCandidatesPt','LeadingTopCandidatePt','SubLeadingTopCandidatePt','HT50'
# histo_list2=['HT_{50} [GeV]']#,'p_{T} fourth AK5 jet'


# cut_list=["Trigger1Histos","Trigger2Histos","Trigger3Histos"]#,"Trigger4Histos","Trigger5Histos"
# trigger_names=["HLT_HT750","HLT_QuadJet50","HLT_HT750||HLT_QuadJet50"]
# base_cut="BaseHistos"



def getEff(name,den,num,rebin=0,xtitle='',ytitle=''):
  c=TCanvas(name+'_Canvas')
  legend=TLegend(0.8,0.1,0.999,0.6)
  legend.SetFillColor(kWhite)
  if rebin!=0:
      den.Rebin(rebin)
      num.Rebin(rebin)
  error_bars=TGraphAsymmErrors()
  error_bars.Divide(num,den,"cl=0.683 b(1,1) mode")
  error_bars.SetLineWidth(3)
  if xtitle=='':
    error_bars.GetXaxis().SetTitle(num.GetXaxis().GetTitle())
  else:
    error_bars.GetXaxis().SetTitle(xtitle)
  if ytitle=='':
    error_bars.GetYaxis().SetTitle(num.GetYaxis().GetTitle())
  else:
    error_bars.GetYaxis().SetTitle(ytitle)
  error_bars.SetLineColor(kBlack)
  error_bars.SetMaximum(1.01)
  error_bars.SetMinimum(0.)
  if ytitle=='':
    error_bars.GetYaxis().SetTitle("Trigger rate")
  else:
    error_bars.GetYaxis().SetTitle(ytitle)
  error_bars.SetTitle('')
  error_bars.Draw('AP')
  c.SaveAs('pdf/'+name+'.pdf')
  c.Write(name+'_Canvas')
  error_bars.Write(name)

def getSF(name,den_data,num_data,den_mc,num_mc,rebin=0,xtitle='',ytitle=''):
  c=TCanvas(name+'_Canvas')
  legend=TLegend(0.8,0.1,0.999,0.6)
  legend.SetFillColor(kWhite)
  if rebin!=0:
      den_mc.Rebin(rebin)
      num_mc.Rebin(rebin)
      den_data.Rebin(rebin)
      num_data.Rebin(rebin)
  num_mc.Divide(den_mc)
  num_data.Divide(den_data)
  num_data.Divide(num_mc)
  num_data.SetLineWidth(3)
  if xtitle=='':
    num_data.GetXaxis().SetTitle(num_data.GetXaxis().GetTitle())
  else:
    num_data.GetXaxis().SetTitle(xtitle)
  if ytitle=='':
    num_data.GetYaxis().SetTitle(num_data.GetYaxis().GetTitle())
  else:
    num_data.GetYaxis().SetTitle(ytitle)
  num_data.SetLineColor(kBlack)
  num_data.SetMaximum(1.5)
  num_data.SetMinimum(0.)
  if ytitle=='':
    num_data.GetYaxis().SetTitle("Scale factor")
  else:
    num_data.GetYaxis().SetTitle(ytitle)
  num_data.SetTitle('')
  num_data.GetXaxis().SetRangeUser(0,2500)
  num_data.Draw('HIST')
  c.SaveAs('pdf/'+name+'.pdf')
  c.Write(name+'_Canvas')
  num_data.Write(name)

getEff('DATA',data_file.Get('Denom/HT'),data_file.Get('Num/HT'),2)
getEff('MC',mc_file.Get('Denom/HT'),mc_file.Get('Num/HT'),2)
getSF('SF',data_file.Get('Denom/HT'),data_file.Get('Num/HT'),mc_file.Get('Denom/HT'),mc_file.Get('Num/HT'))

compare(
  name='DATAMC',
  file_list=[outfile,outfile],
  name_list=['DATA','MC'],
  legend_list=['DATA','MC'],
  drawoption='AP',
  xtitle='HT [GeV]',
  ytitle='Trigger efficiency',
  #minx=0,maxx=0,rebin=1,miny=0,maxy=0,
  textsizefactor=1)

#drawoption2= drawoption.replace("a", "")

#compare('SF',[outfile,outfile],['DATA','MC'],['DATA','MC'])

outfile.Close()

# def getEff2(histo_index,cut_index,rebin=0):
#   c=TCanvas(cut_list[cut_index]+'_'+histo_list[histo_index]+'_Canvas')
#   legend=TLegend(0.8,0.1,0.999,0.6)
#   legend.SetFillColor(kWhite)
#   eff_histos=[]
#   eff_error_bars=[]
#   sample_files=[]
#   for sample_index in range(len(sample_list)):
#     #print path_base+sample_list[sample_index]+'.root'
#     sample_files.append(TFile(path_base+sample_list[sample_index]+'.root'))
#     #print sample_file
#     base_hist=sample_files[-1].Get(base_cut+"/"+histo_list[histo_index]).Clone('base'+sample_list[sample_index]+'_'+cut_list[cut_index]+'_'+histo_list[histo_index])
#     trigger_hist=sample_files[-1].Get(cut_list[cut_index]+"/"+histo_list[histo_index]).Clone(cut_list[cut_index]+'_'+histo_list[histo_index]+'_'+sample_list[sample_index])
#     if rebin!=0:
#       base_hist.Rebin(rebin)
#       trigger_hist.Rebin(rebin)
#     #eff_histos.append(eff_histo)
#     #print sample_list[sample_index]+'_'+cut_list[cut_index]+'_'+histo_list[histo_index]
#     error_bars=TGraphAsymmErrors()
#     error_bars.Divide(trigger_hist,base_hist,"cl=0.683 b(1,1) mode")
#     eff_error_bars.append(error_bars)
#     eff_histos.append(trigger_hist)
#     eff_histos[-1].Divide(trigger_hist,base_hist,1,1,'B')
#     eff_histos[-1].SetStats(kFALSE)
#     eff_histos[-1].SetLineWidth(3)
#     eff_histos[-1].GetXaxis().SetTitle(histo_list2[histo_index])
#     eff_histos[-1].SetLineColor(colors[sample_index])
#     eff_histos[-1].SetMaximum(1.01)
#     eff_histos[-1].SetMinimum(0.)
#     eff_histos[-1].GetYaxis().SetTitle("Trigger rate")
#     eff_histos[-1].SetTitle(trigger_names[cut_index])
    
#     eff_error_bars[-1].SetLineWidth(3)
#     eff_error_bars[-1].GetXaxis().SetTitle(histo_list2[histo_index])
#     eff_error_bars[-1].SetLineColor(colors[sample_index])
#     eff_error_bars[-1].SetMaximum(1.01)
#     eff_error_bars[-1].SetMinimum(0.)
#     eff_error_bars[-1].GetYaxis().SetTitle("Trigger rate")
#     eff_error_bars[-1].SetTitle(trigger_names[cut_index])
    
#     legend.AddEntry(eff_histos[-1],sample_names[sample_index],'l')
#     if len(eff_histos)==1:
#       c.cd()
#       #eff_histos[-1].Draw('AXIS')
#       eff_error_bars[-1].Draw('AP')
#     else:
#       c.cd()
#       #eff_histos[-1].Draw('SAME')
#       eff_error_bars[-1].Draw('PSAME')
#     c2=TCanvas(cut_list[cut_index]+'_'+histo_list[histo_index]+'_'+sample_list[sample_index]+'_Canvas')
#     #eff_histos[-1].Draw('AXIS')
#     eff_error_bars[-1].Draw('AP')
#     #eff_error_bars[-1].Write()
#     legend2=TLegend(0.8,0.2,0.999,0.93)
#     legend2.AddEntry(eff_histos[-1],sample_list[sample_index],'l')
#     legend2.Draw()
#     c2.SaveAs("pdf/"+cut_list[cut_index]+'_'+histo_list[histo_index]+'_'+sample_list[sample_index]+".pdf")
#     outfile.cd()
#     eff_histos[-1].Write()
#     c2.Write()
  
#   c.cd()
#   legend.Draw()
#   c.SaveAs("pdf/"+cut_list[cut_index]+'_'+histo_list[histo_index]+".pdf")
#   outfile.cd()
#   c.Write()