import ROOT  # must be first
import sys
import importlib
import logging
import warnings
import numpy as np
import torch
from torch import nn, utils
from sklearn.preprocessing import StandardScaler

# -----------------------------
# Lightning import (robust)
# -----------------------------
try:
    import lightning as L
except ImportError:
    try:
        import pytorch_lightning as L
    except ImportError:
        L = None

# -----------------------------
# Silence noise
# -----------------------------
warnings.filterwarnings("ignore")
if L:
    logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)

# -----------------------------
# Utility
# -----------------------------
def check_version(package_name, import_name=None):
    name = import_name if import_name else package_name
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", "Detected")
        return "SUCCESS", version
    except ImportError:
        return "FAILED", "Not Found"

# -----------------------------
# Main test suite
# -----------------------------
def run_suite():
    print("=" * 90)
    print("HEP ML ENVIRONMENT VERIFICATION (STRICT)")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Torch CUDA Available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    print("=" * 90)

    # =========================================================
    # 1. PACKAGE CHECK
    # =========================================================
    print("\n[1] PACKAGE AVAILABILITY")
    print(f"{'PACKAGE':<25} | {'STATUS':<10} | VERSION")
    print("-" * 90)

    packages = [
        ("pandas", None),
        ("tables", "tables"),
        ("numba", None),
        ("scipy", None),
        ("matplotlib", None),
        ("seaborn", None),
        ("sklearn", "sklearn"),
        ("xgboost", None),
        ("shap", None),
        ("uproot", None),
        ("mplhep", None),
        ("h5py", None),
        ("wandb", None),
        ("FrEIA", None),
    ]

    for pkg, imp in packages:
        status, version = check_version(pkg, imp)
        print(f"{pkg:<25} | {status:<10} | {version}")

    # Lightning
    if L:
        ver = getattr(L, "__version__", "Unknown")
        ok = "SUCCESS" if ver.startswith("2.") else "VERSION MISMATCH"
        print(f"{'lightning':<25} | {ok:<10} | {ver}")
    else:
        print(f"{'lightning':<25} | FAILED     | Not installed")

    # =========================================================
    # 2. TORCH GPU TEST
    # =========================================================
    print("\n[2] TORCH GPU TEST")
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        x = torch.randn(100, 100).to(device)
        y = torch.matmul(x, x)
        print(f"Torch compute on {device.upper()}: SUCCESS")
    except Exception as e:
        print(f"Torch GPU test: FAILED | {e}")

    # =========================================================
    # 3. ROOT JIT TEST
    # =========================================================
    print("\n[3] ROOT C++ JIT TEST")
    try:
        ROOT.gInterpreter.Declare("""
        #include <cmath>
        #include "TVector2.h"

        namespace HEPTools {
            double DeltaR(double eta1, double phi1, double eta2, double phi2) {
                double deta = eta1 - eta2;
                double dphi = TVector2::Phi_mpi_pi(phi1 - phi2);
                return std::sqrt(deta*deta + dphi*dphi);
            }
        }
        """)

        val = ROOT.HEPTools.DeltaR(0.1, 0.2, 0.4, 0.5)
        print(f"ROOT JIT: SUCCESS | DeltaR = {val:.4f}")
    except Exception as e:
        print(f"ROOT JIT: FAILED | {e}")

    # =========================================================
    # 4. ROOT ↔ NUMPY BRIDGE
    # =========================================================
    print("\n[4] ROOT ↔ NUMPY BRIDGE")
    try:
        vec = ROOT.std.vector('double')()
        for i in range(5):
            vec.push_back(i)

        arr = np.array(list(vec))
        print(f"Bridge SUCCESS | {arr}")
    except Exception as e:
        print(f"Bridge FAILED | {e}")

    # =========================================================
    # 5. UPROOT I/O TEST
    # =========================================================
    print("\n[5] UPROOT I/O TEST")
    try:
        import uproot
        f = uproot.recreate("test.root")
        f["tree"] = {"x": np.random.randn(10)}
        print("uproot write: SUCCESS")
    except Exception as e:
        print(f"uproot write: FAILED | {e}")

    # =========================================================
    # 6. LIGHTNING TRAINING TEST
    # =========================================================
    print("\n[6] LIGHTNING TRAINING TEST")

    if L is None:
        print("Lightning not installed → SKIPPED")
    else:
        try:
            X = np.random.randn(200, 5)
            y = (X[:, 0] > 0.5).astype(int)

            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            dataset = utils.data.TensorDataset(
                torch.tensor(X, dtype=torch.float32),
                torch.tensor(y, dtype=torch.long)
            )

            loader = utils.data.DataLoader(dataset, batch_size=16)

            class TestModel(L.LightningModule):
                def __init__(self):
                    super().__init__()
                    self.layer = nn.Linear(5, 2)
                    self.loss_fn = nn.CrossEntropyLoss()

                def training_step(self, batch, batch_idx):
                    x, y = batch
                    logits = self.layer(x)
                    loss = self.loss_fn(logits, y)
                    return loss

                def configure_optimizers(self):
                    return torch.optim.Adam(self.parameters(), lr=1e-3)

            device = "gpu" if torch.cuda.is_available() else "cpu"

            trainer = L.Trainer(
                max_epochs=2,
                accelerator=device,
                devices=1,
                logger=False,
                enable_progress_bar=False
            )

            trainer.fit(TestModel(), loader)

            print(f"Lightning training: SUCCESS on {device.upper()}")

        except Exception as e:
            print(f"Lightning training: FAILED | {e}")

    print("\n" + "=" * 90)
    print("ALL TESTS COMPLETED")
    print("=" * 90)


if __name__ == "__main__":
    run_suite()
