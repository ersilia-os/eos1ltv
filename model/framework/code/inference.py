import glob
import os
import sys

import numpy as np
import torch
from rdkit import Chem
from rdkit.Chem import AllChem

from simg.model_utils import pipeline, gnn
from simg.data import get_connectivity_info

_CONDA_PREFIX = os.path.dirname(os.path.dirname(sys.executable))
_OBABEL_BIN = os.path.join(_CONDA_PREFIX, "bin", "obabel")

def _ensure_babel_env():
    if not os.path.exists(_OBABEL_BIN):
        return
    if not os.path.isdir(os.environ.get("BABEL_LIBDIR", "")):
        lib_dirs = sorted(glob.glob(os.path.join(_CONDA_PREFIX, "lib", "openbabel", "*")))
        if lib_dirs:
            os.environ["BABEL_LIBDIR"] = lib_dirs[-1]
    if not os.path.isdir(os.environ.get("BABEL_DATADIR", "")):
        data_dirs = sorted(glob.glob(os.path.join(_CONDA_PREFIX, "share", "openbabel", "*")))
        if data_dirs:
            os.environ["BABEL_DATADIR"] = data_dirs[-1]

_ensure_babel_env()

# fixed seed so the 3D conformer, and therefore the embedding, is reproducible
SEED = 42

def smiles_to_xyz(smi: str) -> str:
    mol = Chem.AddHs(Chem.MolFromSmiles(smi))
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    if AllChem.EmbedMolecule(mol, params) != 0:
        # fallback for molecules that fail the standard embedding
        params.useRandomCoords = True
        if AllChem.EmbedMolecule(mol, params) != 0:
            # some caged or bridged molecules only embed without enforcing chirality
            params.enforceChirality = False
            AllChem.EmbedMolecule(mol, params)
    AllChem.MMFFOptimizeMolecule(mol)
    return Chem.MolToXYZBlock(mol)

def get_molecular_representation(smi: str, pooling: str = "atom_mean"):
    xyz = smiles_to_xyz(smi)

    xyz_data = [l + "\n" for l in xyz.split("\n")[2:-1]]
    symbols = [l.split()[0] for l in xyz_data]
    coordinates = np.array(
        [[float(num) for num in l.strip().split()[1:]] for l in xyz_data]
    )
    connectivity = get_connectivity_info(xyz_data)

    graph, lps, interactions, preds = pipeline(symbols, coordinates, connectivity)
    with torch.no_grad():
        node_embeddings = gnn.get_embedding(graph.x, graph.edge_index, graph.edge_attr)

    node_embeddings = node_embeddings.cpu().numpy()

    result = {"graph": graph, "node_embeddings": node_embeddings}

    if pooling == "atom_mean":
        atom_mask = graph.is_atom.bool().numpy()
        result["representation"] = node_embeddings[atom_mask].mean(axis=0)
    elif pooling == "all_mean":
        result["representation"] = node_embeddings.mean(axis=0)

    return result
