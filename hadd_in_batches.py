import glob
from math import ceil
import subprocess
files = sorted(glob.glob("/eos/user/g/glavizza/nanoAOD/WWjjTolnulnu_SS_EFTdim6/root/*.root"))
print(len(files))
print(files)

nFilesToMerge = 100
commands = []
folder = "/eos/user/g/glavizza/nanoAOD/WWjjTolnulnu_SS_EFTdim6/rootHadded"
for i in range(int(ceil(float(len(files))/float(nFilesToMerge)))):
    commands.append("haddnano.py {}/nanoAOD_SSWW_EFTdim6_{}.root {}\n\n".format(folder, i," ".join(files[i*nFilesToMerge:(i+1)*nFilesToMerge])))
    commands.append("ls {}/nanoAOD_SSWW_EFTdim6_{}.root\n\n".format(folder, i))
#print (commands)
print(commands[-1])
with open("merge_SSWW_EFTdim6.sh", "w") as file:
    file.write("#!/bin/bash\n\n")
    file.write("cd ~/CMSSW_10_6_4/src; eval `scramv1 runtime -sh`; cd -;\n\n")
    file.writelines(commands)
p = subprocess.Popen("chmod +x merge_SSWW_EFTdim6.sh", shell=True)
p.wait()
