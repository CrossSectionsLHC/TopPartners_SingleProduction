#!/usr/bin/env 
import pandas as pd
import numpy as np
import time
from array import array
import seaborn as sns
# based on https://gitlab.cern.ch/cms-b2g/diboson-combination/combination-2016/-/blob/master/hvt.py

import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep

#######################################
# Xsec to check  https://www.semanticscholar.org/paper/Handbook-of-vectorlike-quarks%3A-Mixing-and-single-Aguilar-Saavedra-Benbrik/25211cedb816a10c03926f7e60f11a86aba9e30b/figure/5
# For diagrams https://indico.in2p3.fr/event/14083/contributions/16649/attachments/13883/17048/Carvalho_Top_Marseille.pdf
####################################################

# Plot the sigHat's
cZ0 = 0.370349
cW0	= 0.458486
# plot sigHats
colors = ["r", "b", "m", "g", "y", "c"]
counter = 0
fig = plt.figure()
ax = fig.add_subplot()
for part_type in ["T", "B", "Y", "X"] :
    nwa_xs_file = "Single%s/CrossSections_BR_Single%s_NWA.csv" % (part_type, part_type)
    df_nwa_xs_file = pd.read_csv(nwa_xs_file)

    #print(nwa_xs_file)
    #print(df_nwa_xs_file.columns)
    sigHats = [name for name in df_nwa_xs_file.columns  if "(pb)" in name]
    #print(sigHats)
    for ss,sigHat in enumerate(sigHats):
        #print(sigHat)
        QCDscaleUp = "%sQCDscaleUp" % sigHat.replace("(pb)", "") + ("(%)")
        QCDscaleDown = "%sQCDscaleDown" % sigHat.replace("(pb)", "") + ("(%)")
        df_nwa_xs_file["XS_Up"] = df_nwa_xs_file[sigHat]*(1+df_nwa_xs_file[QCDscaleUp]/100)
        df_nwa_xs_file["XS_Down"] = df_nwa_xs_file[sigHat]*(1+df_nwa_xs_file[QCDscaleDown]/100)
        #print(df_nwa_xs_file[[sigHat, QCDscaleUp, QCDscaleDown]])
        if "B" in sigHat :
            linestyle = ":"
        elif "Y" in sigHat :
            linestyle = "--"
        else:
            linestyle = "-"
        plt.plot(
            df_nwa_xs_file["mass"].values, 
            df_nwa_xs_file[sigHat].values, 
            linestyle, 
            label=sigHat.replace("sigmaHat(","").replace(")(pb)",""),
            color=colors[counter] )
        plt.fill_between(
            df_nwa_xs_file["mass"].values,
            df_nwa_xs_file["XS_Up"].values, 
            df_nwa_xs_file["XS_Down"].values, alpha=0.2, color=colors[counter]
            )
        counter += 1
    # making sigmaHats from couplings file

plt.xlabel("VLQmass (GeV)")
plt.ylabel("sigmaHat (pb)")
 
plt.yscale('log')
#plt.scale('log')
plt.legend(loc='lower left', ncol=1) #, bbox_to_anchor=(-0.1,1.15),  frameon=True, edgecolor='black',framealpha=1,fancybox=False, ncol=4) 

nameout = "check_figures/sigHat"
for typePlot in ["pdf", "png"]:
    plt.savefig("%s.%s" % (nameout, typePlot))
    print("Saved XCheck figure %s.%s" % (nameout, typePlot))
plt.clf()

################### 
# Plot couplings
###################
# sigmaHat(Xtj)(pb) sigmaHat(Ybj)(pb) sigmaHat(Btj)(pb) sigmaHat(Bbj)(pb) sigmaHat(Ttj)(pb) sigmaHat(Tbj)(pb)

for part_type in ["T", "B", "Y", "X"] :
    nwa_coupling_file = "Single%s/Coupling_x_FixedTotalWidth_Single%s_NWA.csv" % (part_type, part_type)
    df_nwa_coupling_file = pd.read_csv(nwa_coupling_file)
    print(nwa_coupling_file)
    print(df_nwa_coupling_file.columns)
    #print(df_nwa_coupling_file)

    ## Drawing all the couplings
    if part_type == "X" or part_type == "Y" :
        gammas = ['G/MQ=1%', 'G/MQ=2%', 'G/MQ=3%', 'G/MQ=4%', 'G/MQ=5%']
    elif part_type == "B" :
        gammas = [
            'G/MQ=1%(singlet)', 'G/MQ=2%(singlet)', 'G/MQ=3%(singlet)', 'G/MQ=4%(singlet)', 'G/MQ=5%(singlet)', 
            'G/MQ=1%(doublet)', 'G/MQ=2%(doublet)', 'G/MQ=3%(doublet)', 'G/MQ=4%(doublet)', 'G/MQ=5%(doublet)',
            ]
    if part_type == "T" :
        gammas = [
            'G/MQ=1%(singlet)', 
            'G/MQ=2%(singlet)', 
            'G/MQ=3%(singlet)', 
            'G/MQ=4%(singlet)', 
            'G/MQ=5%(singlet)', 
            'G/MQ=1%(doublet)', #'G/MQ=1%(doublet2)',
            'G/MQ=2%(doublet)', #'G/MQ=1%(doublet2).1',
            'G/MQ=3%(doublet)', #'G/MQ=1%(doublet2).2',
            'G/MQ=4%(doublet)', #'G/MQ=1%(doublet2).3',
            'G/MQ=5%(doublet)', #'G/MQ=1%(doublet2).4',
            ]

    fig = plt.figure()
    ax = fig.add_subplot()
    for gamma in gammas :
        print(gamma)

        if "singlet" in gamma :
            linestyle = ":"
        elif "doublet" in gamma :
            linestyle = "-"
        #else:
        #    linestyle = "-"

        if "1%" in gamma :
            color = "r"
        elif "2%" in gamma :
            color = "b"
        elif "3%" in gamma :
            color = "g"
        elif "4%" in gamma :
            color = "m"
        elif "5%" in gamma :
            color = "y"

        plt.plot(
            df_nwa_coupling_file["mass"].values, 
            df_nwa_coupling_file[gamma].values, 
            linestyle, 
            label=gamma,
            color=color
            )        

    plt.legend(loc='upper right', ncol=2) #, bbox_to_anchor=(-0.1,1.15),  frameon=True, edgecolor='black',framealpha=1,fancybox=False, ncol=4) 

    plt.xlabel("VLQmass (GeV)")
    plt.ylabel("coupling")

    nameout = "check_figures/couplings_%s" % part_type
    for typePlot in ["pdf", "png"]:
        plt.savefig("%s.%s" % (nameout, typePlot))
        print("Saved XCheck figure %s.%s" % (nameout, typePlot))
    plt.clf()

    ## making tables and plots with Xsec
    ## Take the correct Xsec tables

    ## Drawing all the couplings
    if part_type == "Y" :
        gammas = [
            'G/MQ=1%', 'G/MQ=2%', 'G/MQ=3%', 
            ]
        procs = {
            "Ybj" : cW0
            }
    elif part_type == "X" :
        gammas = [
            'G/MQ=1%', 'G/MQ=2%', 'G/MQ=3%', 
            #'G/MQ=4%', 
            #'G/MQ=5%'
            ]
        procs = {
            "Xtj" : cW0
            }
    elif part_type == "B" :
        gammas = [
            'G/MQ=1%(singlet)', 'G/MQ=2%(singlet)', 'G/MQ=3%(singlet)', 'G/MQ=4%(singlet)', 'G/MQ=5%(singlet)', 
            'G/MQ=1%(doublet)', 'G/MQ=2%(doublet)', 'G/MQ=3%(doublet)', 'G/MQ=4%(doublet)', 'G/MQ=5%(doublet)',
            ]
        procs = {
            "Bbj" : cZ0, 
            "Btj" : cW0
            }
    if part_type == "T" :
        gammas = [
            'G/MQ=1%(singlet)', 
            'G/MQ=2%(singlet)', 
            'G/MQ=3%(singlet)', 
            'G/MQ=4%(singlet)', 
            'G/MQ=5%(singlet)', 
            'G/MQ=1%(doublet)', #'G/MQ=1%(doublet2)',
            'G/MQ=2%(doublet)', #'G/MQ=1%(doublet2).1',
            'G/MQ=3%(doublet)', #'G/MQ=1%(doublet2).2',
            #'G/MQ=4%(doublet)', #'G/MQ=1%(doublet2).3',
            'G/MQ=5%(doublet)', #'G/MQ=1%(doublet2).4',
            ]
        procs = {
            "Tbj" : cW0, 
            "Ttj" : cZ0
            }


    nwa_xs_file = "Single%s/CrossSections_BR_Single%s_NWA.csv" % (part_type, part_type)
    df_nwa_xs_file = pd.read_csv(nwa_xs_file)
    print(df_nwa_xs_file.columns)

    df_with_couplings = pd.DataFrame()
    df_with_couplings["mass"] = df_nwa_xs_file["mass"]
    df_with_couplings["mass1"] = df_with_couplings["mass"]

    for pp, proc in enumerate(procs):
        fig = plt.figure()
        ax = fig.add_subplot()
        #else:
        #    linestyle = "-"


        ### save file by process
        for gamma in gammas :

            if "singlet" in gamma :
                linestyle = ":"
            elif "doublet" in gamma :
                linestyle = "-"

            if "1%" in gamma :
                color = "r"
            elif "2%" in gamma :
                color = "b"
            elif "3%" in gamma :
                color = "g"
            elif "4%" in gamma :
                color = "m"
            elif "5%" in gamma :
                color = "y"

            print(proc, procs[proc])
            center = 'sigmaHat(%s)(pb)_%s' % (proc, gamma) 
            up = 'sigmaHat(%s)Up(pb)_%s' % (proc, gamma)
            down = 'sigmaHat(%s)Down(pb)_%s' % (proc, gamma)

            df_with_couplings[center] = df_nwa_xs_file['sigmaHat(%s)(pb)' % (proc) ]*(procs[proc]*df_nwa_coupling_file[gamma])**2
            #df_with_couplings['@@sigmaHat(%s)(pb)_%s' % (proc, gamma) ] = (df_nwa_coupling_file[gamma])
            df_with_couplings[up] = df_with_couplings['sigmaHat(%s)(pb)_%s' % (proc, gamma) ]*(1+df_nwa_xs_file['sigmaHat(%s)QCDscaleUp' % proc + '(%)']/100) 
            df_with_couplings[down] = df_with_couplings['sigmaHat(%s)(pb)_%s' % (proc, gamma) ]*(1+df_nwa_xs_file['sigmaHat(%s)QCDscaleDown' % proc + '(%)']/100) # 'sigmaHat(Tbj)QCDscaleDown(%)'

            plt.plot(
                df_with_couplings["mass"].values, 
                df_with_couplings[center].values, 
                linestyle, 
                label=center.replace("sigmaHat(","").replace(")(pb)",""),
                color=color)
            plt.fill_between(
                df_with_couplings["mass"].values,
                df_with_couplings[up].values, 
                df_with_couplings[down].values, alpha=0.2, 
                color=color
                )

            plt.xlabel("VLQmass (GeV)")
            plt.ylabel("sigma (pb)")
            
            plt.yscale('log')
            #plt.scale('log')
            plt.legend(loc='lower left', ncol=2) #, bbox_to_anchor=(-0.1,1.15),  frameon=True, edgecolor='black',framealpha=1,fancybox=False, ncol=4) 

        nameout = "check_figures/sigmas_%s_%s" % (part_type, proc)
        for typePlot in ["pdf", "png"]:
            plt.savefig("%s.%s" % (nameout, typePlot))
            print("Saved XCheck figure %s.%s" % (nameout, typePlot))
        plt.clf()


    print(df_with_couplings)
    print("---------------------------")


#    df_nwa_coupling_file = pd.read_csv(nwa_coupling_file)
#    df_nwa_xs_file = pd.read_csv(nwa_xs_file)
