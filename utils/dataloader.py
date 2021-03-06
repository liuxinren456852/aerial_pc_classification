import torch
from torch.utils.data import Dataset
import numpy as np
from utils.ply import ply2dict
from sklearn.neighbors import KDTree


class AerialPointDataset(Dataset):
    def __init__(self, file, k):
        "Initialization"
        data = ply2dict(file)
        self.X = torch.from_numpy(
            np.vstack(
                (
                    data["x"],
                    data["y"],
                    data["z"],
                    data["height_above_ground"],
                    data["planarity"],
                    data["curvature"],
                    data["sphericity"],
                    data["verticality"],
                )
            ).T
        )
        self.labels = torch.from_numpy(data["labels"])
        self.n_samples = self.labels.shape[0]
        tree = KDTree(self.X[:, :3])
        _, self.inds = tree.query(self.X[:, :3], k=k)

    def __getitem__(self, index):
        return (
            torch.cat(
                (self.X[index].view(1, -1), self.X[self.inds[index]]), 0
            ),
            self.labels[index],
        )

    def __len__(self):
        return self.n_samples
