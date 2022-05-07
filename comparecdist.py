#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## comparebdist.py
import matplotlib.pyplot as plt
from globalplotvar import Bins,variables,tracksel
import os
from multiprocessing import Pool
from cycler import cycler
import numpy as np


base_path=str("/home/sammy/eos/user/s/sgoswami/public/NN_SRC_DATA/")

input_file_std_dl = base_path+ "ttbar/std/refined_std_tightuser.sgoswami.28416367._000237.output.h5"
input_file_lrt_dl = base_path+ "ttbar/lrt/refined_lrt_tightuser.sgoswami.28415580._000203.output.h5"
input_file_std_ll = base_path+ "ttbar_30_30/std/user.sgoswami.28416367._000237.output.h5"
input_file_lrt_ll = base_path+ "ttbar_30_30/lrt/user.sgoswami.28415580._000203.output.h5"
 
# a refers to the file input list in that order
a = [input_file_std_dl,input_file_lrt_dl,input_file_std_ll,input_file_lrt_ll]
# b refers to the flavor needed for each file
b = [4]*4

inputs = [f'{a[i]} {b[i]} '.split() for i in range(0,4)]
print("Inputs=", inputs)

outputs=[]
with Pool(processes=16) as pool:
    outputs = np.array(pool.starmap(tracksel, inputs))
    pool.close()
    pool.join()

print("The shape of the output is:",outputs.shape)

os.makedirs('cplots_new_compare',exist_ok = True)
os.chdir('cplots_new_compare')

for vartype in variables:
    print("The vartype is: "+ vartype+ "\n")
    for var in variables[vartype]:
        print("The var is: "+ var +"\n")
        
        plt.clf()
        fig,ax=plt.subplots(4,1,sharex=True)
        plt.figure(figsize=(20,10)) 
        plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'k'])))
	
        val_of_bins   =[0]*(len(a))
        edges_of_bins =[0]*(len(a))
        patches       =[0]*(len(a))
        labels        =["STD (c-jets): d0=3.5mm, z0=5mm",
                        "STD+LRT (c-jets): d0=3.5mm, z0=5mm",
                        "STD (c-jets): d0=30mm, z0=30mm",
                        "STD+LRT (c-jets): d0=30mm, z0=30mm"
                        ]
        
        ratio_labels  =["STD ratio: LRT loose to DIPS loose",
                        "STD+LRT ratio: LRT loose to DIPS loose",
                        "STD+LRT to STD ratio: DIPS loose"
                        ]
        
        for k in range(0,len(a)):
            val_of_bins[k], edges_of_bins[k], patches[k] =ax[0].hist(outputs[k][var],bins = Bins[var], histtype='step', alpha=0.5, label=labels[k])
        
        pltratio=[np.abs(np.true_divide(val_of_bins[i+2],val_of_bins[i],where=(val_of_bins[i] != 0))) for i in range(0,2)]
        pltratio.append(np.abs(np.true_divide(val_of_bins[1],val_of_bins[0],where=(val_of_bins[0] != 0))))
        bincenter =[(0.5 * (edges_of_bins[i][1:] + edges_of_bins[i][:-1])) for i in range(0,len(a))]

        ax[0].legend(loc='best',fontsize=7,framealpha=0.2)
        ax[0].set_xlabel(var, size=7)
        ax[0].set_ylabel("Distribution", size=7)
        ax[0].set_yscale('log')
        ax[0].grid(True)
       
        for k in range(0,2):
            ax[k+1].errorbar(bincenter[k], pltratio[k], yerr=None, color='r', fmt='.',label=ratio_labels[k])
            ax[k+1].legend(loc='best',fontsize=7,framealpha=0.2)
            ax[k+1].set_yscale('log')
            ax[k+1].grid(True)
        
        ax[3].errorbar(bincenter[1], pltratio[2], yerr=None, color='r', fmt='.',label=ratio_labels[2])
        ax[3].legend(loc='best',fontsize=7,framealpha=0.2)
        ax[3].set_yscale('log')
        ax[3].grid(True)

        plname=str(var)+'_charm.png'
        fig.savefig(plname,bbox_inches="tight")
        plt.close()
        print("Savefig block done for "+var+".\n")

