__author__ = 'Zhenbang Yu'
__copyright__ = 'Copyright 2022, Zhenbang Yu'
__email__ = 'roger_yu@berkeley.edu'

# import flask relevant packages.
from flask import Flask, url_for, render_template, redirect, request

# import useful packages
import json
import pickle
import numpy as np
import os
from collections import OrderedDict
import pandas as pd

# import useful packages in original StoichiometryFitter
import ReportResults
import imp
import PhysicsBasics as pb
import CountsToQuantWeb
import PhaseFit

# Stoich = pd.read_csv("ConfigData/stoich Silicates.csv")
Stoich = np.genfromtxt('ConfigData/stoich Silicates.csv', dtype=None, comments='#', delimiter=',', skip_header=1, converters={1: lambda s: float(s)})


# initiate flask app
app = Flask(__name__)

# Everything in here.
@app.route('/', methods = ["POST","GET"])
def login():
    if request.method == "POST":
        # print("False")
        Counts = np.zeros(118)
        charge = {}

        element = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Uus","Uuo"]
        for i in range(len(element)):
            Counts[i] = request.form[element[i]+"1"]
        InputDat = OrderedDict(list(zip(element, Counts)))
        # print(InputDat)
        ReportStr1 = ReportResults.FormatInputResults(InputDat, "Counts")
        # print(ReportStr1)
        # Find out if there is a k-factor file to use.
        if request.form.get("k-factor"):
            kfacsfile = request.form["k-value"]
        else:
            kfacsfile = None

        # Find out if there is an absorption correction to use.
        if request.form.get("arbitraryAnalysis"):
            DetectorFile = request.form["arbitrary"]
            # print(absorption)
        else:
            DetectorFile = None

        # Find out if there is an absorption correction to do.
        if request.form.get("TEM"):
            try:
                # The text box uses nm.  Absorption path lengths are in microns, convert.
                AbsorptionCorrection = float(request.form["density"])/1000
                Takeoff = np.clip(float(request.form["degree"]), 0.1, 90) # Allow angles between 0.1 and 90 degrees.
                # AbsorptionCorrection = request.form["density"]
                # Takeoff = request.form["degree"]
            except:
                # Error Message
                print("Error")
                return render_template('login.html')
        else:
            AbsorptionCorrection = 0
            Takeoff = 18

        # Find out if we are using oxygen by stoichiometry
        if request.form.get("oxygen"):
            # Stoich is a list of tuples.  We want an array of atom charges from the 1 index of the tuples.  So unzip
            # the list into two tuples,
            # choose the tuple which corresponds to the charges not the atom names and feed it to numpy to make a vector.
            OByStoich = np.array(list(zip(*Stoich))[1])
            # OByStoich = request.form["k-value2"]
        else:
            OByStoich = None

        # Stuff the user entered data into a black box and get out At%, Wt% results.
        Quant = CountsToQuantWeb.GetAbundancesFromCounts(Counts, kfacsfile=kfacsfile, InputType= "Counts", ArbitraryAbsorptionCorrection=DetectorFile, AbsorptionCorrection=AbsorptionCorrection, Takeoff=Takeoff, OByStoichiometry=OByStoich)
                                                        
        QuantNumbers = [a[1] for a in list(Quant.items())]
        AtPct, WtPct, OxWtPct, kfactors = list(zip(*QuantNumbers))
        # print(Counts)
        # print(kfacsfile)
        # print(DetectorFile)
        # print(AbsorptionCorrection)
        # print(Takeoff)
        # print(OByStoich)
        # print(Quant)
        # print(AtPct, WtPct, OxWtPct, kfactors)

        ReportStr2 = ReportResults.FormatQuantResults(Quant, ArbitraryAbsorptionCorrection=DetectorFile, AbsorptionCorrection=AbsorptionCorrection,Takeoff=Takeoff,OByStoichiometry=OByStoich,kFactors=kfacsfile)
        #print(ReportStr2)

        """ DO CUSTOM PHASE ANALYSES """
        if request.form.get("phaseAnalysis"):
            # Construct the name of the py file containing the analysis function.
            PhaseFile = request.form["phase"]
            PhaseFile = 'ConfigData/phase ' + PhaseFile + '.py'

            # import it and run it.
            a = imp.load_source('AnalyzePhase', PhaseFile)
            ReportStr3 = a.AnalyzePhase(AtPct, WtPct, OxWtPct, OByStoich)
        else:
            ReportStr3 = ""

        for i in element:
            charge[i] = request.form[i+"2"]
        
        FinalReport = ReportStr1 + ReportStr2 + ReportStr3
        print(FinalReport)
        FinalReport = FinalReport.replace("\n", "<br>")
        
        
        return render_template('result.html', charge=charge, mylist=Counts, absorption=DetectorFile, degree = Takeoff, density = AbsorptionCorrection, k_factor = kfacsfile, OByStoich = OByStoich, Result = FinalReport)
        #return redirect(url_for("user", usr = phase))
    else:
        Stoich2 = np.genfromtxt('ConfigData/stoich Silicates.csv', dtype=None, comments='#', delimiter=',', skip_header=1, converters={1: lambda s: float(s)})
        Stoich3 = []
        for i in range(len(Stoich2)):
            Stoich3.append(Stoich2[i][1])
            # print(Stoich2[i][1])
        Stoich3 = json.dumps(Stoich3)
        return render_template('login.html', Stoich = Stoich3)

@app.route("/<usr>")
def user(usr):
    return f"<h1>This is the dictionary{usr}</h1>"

if __name__ == '__main__':
    app.run(debug = True)