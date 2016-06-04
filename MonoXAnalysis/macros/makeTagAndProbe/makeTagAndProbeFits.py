#python makeTagAndProbeFits.py --inputDIR /home/rgerosa/MONOJET_ANALYSIS/TagAndProbe_600pb-1/SingleMuon/ --outputDIR testFit --typeID looseid --leptonType muon 
import os
import glob
import math
from array import array
import sys
import time
import subprocess
import ROOT

from optparse import OptionParser
from subprocess import Popen

############################################                                                                                                                                 
#            Job steering                  #                                                                                                                                 
############################################                                                                                                                                   

muonPtBinning  = [10.0,20.0,30.0,40.0,50.0,700.,200.0];
muonEtaBinning = [0.0,1.2,2.4]

electronPtBinning  = [10.0,20.0,30.0,40.0,50.0,70.0,200.0];
electronEtaBinning = [0.0,1.5,2.5];

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')

## parse files                                                                                                                                                                 
parser.add_option('--inputDIR',     action="store", type="string", dest="inputDIR",     default="",   help="input directory where files are contained")
parser.add_option('--outputDIR',    action="store", type="string", dest="outputDIR",    default="",   help="output DIR")
parser.add_option('--isMC',         action="store_true",           dest="isMC",                       help="isMC")
parser.add_option('--typeID',       action="store", type="string", dest="typeID",       default="",   help="lepton id type: looseid or tightid for muons, vetoid or tightid for electrons")
parser.add_option('--leptonType',   action="store", type="string", dest="leptonType",   default="",   help="lepton type: muon or electron")

##  for submitting jobs in lxbatch
parser.add_option('--batchMode',    action="store_true",           dest="batchMode",                  help="batchMode")
parser.add_option('--jobDIR',       action="store", type="string", dest="jobDIR",  default="",        help="directory for job")
parser.add_option('--queque',       action="store", type="string", dest="queque",  default="",        help="queque for LSF")
parser.add_option('--submit',       action="store_true",           dest="submit",                     help="submit")

(options, args) = parser.parse_args()

if __name__ == '__main__':

    isMC = False;
    if options.isMC == True:
        isMC = True;

    if not options.batchMode:
        os.system("mkdir -p "+options.outputDIR);

    if options.leptonType == "muon":
        for pt in range(len(muonPtBinning)-1):
            for eta in range(len(muonEtaBinning)-1):
                if not options.batchMode:
                    command = "cmsRun tnpanalysis.py isMC="+str(isMC)+" inputDIR="+options.inputDIR+" outputDIR="+options.outputDIR+" typeID="+options.typeID+" leptonPID="+str(13)+" ptMin="+str(muonPtBinning[pt])+" ptMax="+str(muonPtBinning[pt+1])+" etaMin="+str(muonEtaBinning[eta])+" etaMax="+str(muonEtaBinning[eta+1]);
                    ### look for the template file
                    templatePath = os.path.expandvars('$CMSSW_BASE/src/AnalysisCode/MonoXAnalysis/data/TagAndProbeTemplates')
                    os.system("ls "+templatePath+" | grep root | grep "+options.leptonType+" | grep "+options.typeID+" | grep pt_"+str(muonPtBinning[pt])+"_"+str(muonPtBinning[pt+1])+"_eta_"+str(muonEtaBinning[eta])+"_"+str(muonEtaBinning[eta+1])+" > file_temp_"+options.leptonType+"_"+options.typeID);
                    file = open("file_temp_"+options.leptonType+"_"+options.typeID,"r");
                    listOffile = [];
                    for line in file:
                        if line == "" or line =="\n": continue;
                        listOffile.append(line.replace("\n",""));
                    if len(listOffile) > 1:
                        sys.exit('Problem more than one template file for a single configuration --> return');
                    command += " templateFile="+templatePath+"/"+listOffile[0];
                    os.system(command+" backgroundType=RooCMSShape");
                    os.system(command+" backgroundType=Exponential");
                else:
                    ### to be written
                    print "to be written"
    elif options.leptonType == "electron":
        for pt in range(len(electronPtBinning)-1):
            for eta in range(len(electronEtaBinning)-1):
                if not options.batchMode:
                    command = "cmsRun tnpanalysis.py isMC="+str(isMC)+" inputDIR="+options.inputDIR+" outputDIR="+options.outputDIR+" typeID="+options.typeID+" leptonPID="+str(11)+" ptMin="+str(electronPtBinning[pt])+" ptMax="+str(electronPtBinning[pt+1])+" etaMin="+str(electronEtaBinning[eta])+" etaMax="+str(electronEtaBinning[eta+1])

                    ### look for the template file
                    templatePath = os.path.expandvars('$CMSSW_BASE/src/AnalysisCode/MonoXAnalysis/data/TagAndProbeTemplates')
                    os.system("ls "+templatePath+" | grep root | grep "+options.leptonType+" | grep "+options.typeID+" | grep pt_"+str(electronPtBinning[pt])+"_"+str(electronPtBinning[pt+1])+"_eta_"+str(electronEtaBinning[eta])+"_"+str(electronEtaBinning[eta+1])+" > file_temp_"+options.leptonType+"_"+options.typeID);
                    file = open("file_temp_"+options.leptonType+"_"+options.typeID,"r");
                    listOffile = [];
                    for line in file:
                        if line == "" or line =="\n": continue;
                        listOffile.append(line.replace("\n",""));
                    if len(listOffile) > 1:
                        sys.exit('Problem more than one template file for a single configuration --> return');
                    command += " templateFile="+templatePath+"/"+listOffile[0];
                    ## run first fit with RooCMSShape
                    print command
                    os.system(command+" backgroundType=RooCMSShape");
                    os.system(command+" backgroundType=Exponential");

    else:
        sys.exit('Problem with lepton type --> muon or electron are the recognized options --> exit');

        os.system("rm file_temp_"+options.leptonType+"_"+options.typeID);