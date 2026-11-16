# imports
import os
import csv
import sys
import numpy as np
from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt
from ersilia_pack_utils.core import read_smiles, write_out
from inference import get_molecular_representation
# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# number of embedding features (see columns/run_columns.csv)
N_FEATURES = 128

# my model
def my_model(smiles_list):
    results = []
    print("=="*20)
    for smi in smiles_list:
        try:
            results.append(get_molecular_representation(smi)['representation'])
        except Exception as e:
            # molecules the SIMG pipeline cannot represent (e.g. single ions such as [Y+3],
            # elements outside its atom vocabulary) get an empty row instead of failing the batch
            print(f"Could not process {smi}: {type(e).__name__}: {e}", file=sys.stderr)
            results.append(np.full(N_FEATURES, np.nan, dtype=np.float32))
    return np.array(results)


# read SMILES from .csv file, assuming one column with header
_, smiles_list = read_smiles(input_file)

# run model
outputs = my_model(smiles_list)

#check input and output have the same lenght
input_len = len(smiles_list)
output_len = len(outputs)
assert input_len == output_len

num_dims = outputs.shape[1]
header = [f"feat_{str(i).zfill(3)}" for i in range(num_dims)]

# write output in a .csv file
write_out(outputs, header, output_file, np.float32)
