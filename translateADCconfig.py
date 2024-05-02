mydicADC = {}
for i in range (25):
    mydicADC["ch_"+str(i)] = []

mydicADC1 = {}
for i in range (25):
    mydicADC1["ch_"+str(i)] = []

mydic = {}
mydic["adc0"]= mydicADC
mydic["adc1"]= mydicADC1

mydictt = {}
mydictt["t0"] = mydic





for t in range(1):
    for vfe in range(1,6):
        file_path = "ADCconfig/ADC_config_file_bcp1_t"+str(t)+"_vfe"+str(vfe)+".txt"
        registerADC0 = []
        registerADC1 = []
        with open(file_path, 'r') as f:
            for line in f:
                l = line.strip()
                if l.startswith("#"):
                    continue
                ll = l.split()
                if True:
                    registerADC0.append(int(ll[0]))
                    registerADC1.append(int(ll[1])) # lunga 76 dividi per 5 e hai canali di
        f.close()
        for j in range(5):
#            print (registerADC0[76*j:76*(j+1)])
#            print (registerADC1[76*j:76*(j+1)])
            mydictt["t"+str(t)]["adc0"]["ch_"+str((vfe-1)*5+j)].extend(registerADC0[76*j:76*(j+1)])
            mydictt["t"+str(t)]["adc1"]["ch_"+str((vfe-1)*5+j)].extend(registerADC1[76*j:76*(j+1)])
print (mydictt)
