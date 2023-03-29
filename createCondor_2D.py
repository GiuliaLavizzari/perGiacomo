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

def makeSubmit(op1, op2, opr):
    #########
    file_name = "../fits/fit2D_{}_{}/submit.sh".format(op1,op2)
    f = open(file_name, 'w')
    print (file_name)

    ls_op = list(opr.keys())
    signal_POI = ",".join(["k_"+ str(i) for i in [op1,op2]])
    print (signal_POI)
    other_POI = ",".join(["k_" + str(i) for i in ls_op if i not in [op1,op2]])
    print (other_POI)
    freeze_params = ",".join(["k_"+str(i)+"=1" for i in ls_op if i not in [op1,op2]])
    print (freeze_params)
    signal_ranges = "k_"+str(op1)+"="+str(opr[op1][0])+","+str(opr[op1][1])+":"+"k_"+str(op2)+"="+str(opr[op2][0])+","+str(opr[op2][1])
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
    f.write('combine -M MultiDimFit workspace2D.root --algo=grid --points 5000 -m 125 -t -1 --robustFit=1 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --redefineSignalPOIs {} --freezeParameters r,{} --setParameters r=1,{} --setParameterRanges {} --verbose -1 -n 2D_{}_{} \n'.format(signal_POI, other_POI, freeze_params, signal_ranges, op1, op2))
    f.write("mv higgsCombine2D_{}_{}.MultiDimFit.mH125.root ./fits/\n".format(op1,op2))
    f.write("cd -\n")
    f.close()

    st = os.stat(file_name)
    os.chmod(file_name, st.st_mode | stat.S_IEXEC)

    #########
    file_name_1 = "../fits/submit2D.sub".format(op1,op2)
    f1 = open(file_name_1, 'w')

    f1.write('Universe    = vanilla\n')
    f1.write('Executable  = $(dir)/submit.sh\n')
#    f1.write('initial_dir = $(dir)\n')
    f1.write('output      = $(dir)/submit.out\n')
    f1.write('error       = $(dir)/submit.err\n')
    f1.write('log         = $(dir)/submit.log\n')
    f1.write('queue dir from list2D.txt\n')
    f1.write('+JobFlavour = "espresso"\n')

    f1.close()
    st = os.stat(file_name_1)
    os.chmod(file_name_1, st.st_mode | stat.S_IEXEC)

os.mkdir('../fits')
list_name = "../fits/list2D.txt"
f_ls = open(list_name, 'w')

for i in range(len(opr)):
    for j in range(len(opr)):
        if j > i:
            op1 = list(opr.keys())[i]
            op2 = list(opr.keys())[j]
            os.mkdir("../fits/fit2D_{}_{}".format(op1,op2))
            f_ls.write("fit2D_{}_{}\n".format(op1,op2))
#            print (list(opr.keys())[i],list(opr.keys())[j])
            makeSubmit(op1,op2,opr)

