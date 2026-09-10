import os
import uuid

import numpy as np
import torch

from simg.model_utils import pipeline, gnn
from simg.data import get_connectivity_info

def smiles_to_xyz(smi: str) -> str:
    path = uuid.uuid4().hex
    smi_path = f"{path}.smi"
    xyz_path = f"{path}.xyz"
    with open(smi_path, "w") as f:
        f.writelines(smi + "\n")

    os.system(f"obabel -i smi {smi_path} -o xyz -O {xyz_path} --gen3d >/dev/null 2>&1")

    with open(xyz_path, "r") as f:
        xyz = f.read()
    os.remove(smi_path)
    os.remove(xyz_path)

    return xyz

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
