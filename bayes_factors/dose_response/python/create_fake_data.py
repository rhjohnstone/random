import doseresponse as dr
import numpy as np

drug = "Remitriptyline"
channel = "blERG"

file_name = "../input/ross_data.csv"

concs = np.array([0.0008, 0.08, 0.8, 8.])


with open(file_name,"w") as outfile:
    outfile.write("Compound,Channel,Experiment,Dose,Response\n")