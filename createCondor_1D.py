import os
import sys
from glob import glob
#from configparser import ConfigParser
import numpy as np
import stat

opr = {
    'cW': [-5,5],
    'cHDD' : [-50,20],
    'cHW': [-20,20],
    'cHWB': [-30,30],
    'cHbox': [-10,10],
    'cHj1':[-10,10],
    'cHj3':[-10,10],
    'cHl1' : [-70,70],
    'cHl3' : [-5,5],
    'cll1': [-2,2],
    'cjj11': [-2,2],
    'cjj31': [-1.5,1.5],
    'cjj18': [-5,5],
    'cjj38': [-5,5]
}

def makeSubmit(op1, opr):
    #########
    file_name = "../fits/fit1D_{}/submit.sh".format(op1)
    f = open(file_name, 'w')
    print (file_name)

    ls_op = list(opr.keys())
    signal_POI = ",".join(["k_"+ str(i) for i in [op1]])
    print (signal_POI)
    other_POI = ",".join(["k_" + str(i) for i in ls_op if i not in [op1]])
    print (other_POI)
    freeze_params = ",".join(["k_"+str(i)+"=1" for i in ls_op if i not in [op1]])
    print (freeze_params)
    signal_ranges = "k_"+str(op1)+"="+str(opr[op1][0])+","+str(opr[op1][1])
    print (signal_ranges)

    f.write("#!/bin/sh\n\n")
    f.write("#-----------------------------------\n")
    f.write("#     Automatically generated       # \n")
    f.write("#        by mkDatacard.py           # \n")
    f.write("#-----------------------------------\n")
    f.write("\n\n\n")

#    f.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
#    f.write('eval `scram run -sh`\n')
    f.write('#-----------------------------------\n')
    f.write('cd /afs/cern.ch/user/g/glavizza/private/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling\n')
    f.write('cmsenv\n')
    f.write('combine -M MultiDimFit workspace2D.root --algo=grid --points 500 -m 125 -t -1 --robustFit=1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --redefineSignalPOIs {} --freezeParameters r,{} --setParameters r=1,{} --setParameterRanges {} --verbose -1 -n 1D_{} \n'.format(signal_POI, other_POI, freeze_params, signal_ranges, op1))
    f.write("mv higgsCombine1D_{}.MultiDimFit.mH125.root ./fits/\n".format(op1))
    f.write("cd -\n")
    f.close()

    st = os.stat(file_name)
    os.chmod(file_name, st.st_mode | stat.S_IEXEC)

    #########
    file_name_1 = "../fits/submit1D.sub"
    f1 = open(file_name_1, 'w')

    f1.write('Universe    = vanilla\n')
    f1.write('Executable  = $(dir)/submit.sh\n')
#    f1.write('initial_dir = $(dir)\n')
    f1.write('output      = $(dir)/submit.out\n')
    f1.write('error       = $(dir)/submit.err\n')
    f1.write('log         = $(dir)/submit.log\n')
    f1.write('queue dir from list1D.txt\n')
    f1.write('+JobFlavour = "longlunch"\n')

    f1.close()
    st = os.stat(file_name_1)
    os.chmod(file_name_1, st.st_mode | stat.S_IEXEC)

# os.mkdir('../fits')
list_name = "../fits/list1D.txt"
f_ls = open(list_name, 'w')

for i in range(len(opr)):
    op1 = list(opr.keys())[i]
    os.mkdir("../fits/fit1D_{}".format(op1))
    f_ls.write("fit1D_{}\n".format(op1))
    makeSubmit(op1,opr)

f_ls.close()
