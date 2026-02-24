import sys
import importlib
import logging
import warnings
import numpy as np
import pandas as pd
import torch
from torch import nn, utils
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Robust Lightning Import
try:
    import lightning as L
except ImportError:
    try:
        import pytorch_lightning as L
    except ImportError:
        L = None

# Suppress background noise
warnings.filterwarnings("ignore")
if L:
    logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)

def check_version(package_name, import_name=None):
    name = import_name if import_name else package_name
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", "Detected")
        return "SUCCESS", version
    except ImportError:
        return "FAILED", "Not Found"

def run_suite():
    print("=" * 90)
    print("FORMAL ENVIRONMENT VERIFICATION REPORT - VERSION 2.0")
    print(f"System: Python {sys.version.split()[0]} | Torch GPU: {torch.cuda.is_available()}")
    print("=" * 90)
    
    # --- SECTION 1: PACKAGE AVAILABILITY ---
    print(f"{'PACKAGE':<25} | {'STATUS':<15} | {'VERSION/DETAILS'}")
    print("-" * 90)
    
    packages = [
        ("pandas", None),
        ("pytables", "tables"),
        ("numba", None),
        ("scipy", None),
        ("matplotlib", None),
        ("seaborn", None),
        ("scikit-learn", "sklearn"),
        ("xgboost", None),
        ("shap", None),
        ("uproot", None),
        ("mplhep", None),
        ("h5py", None),
    ]

    for pkg, imp in packages:
        status, details = check_version(pkg, imp)
        print(f"{pkg:<25} | {status:<15} | {details}")

    # Explicit check for Lightning
    if L:
        l_ver = getattr(L, "__version__", "Unknown")
        status = "SUCCESS" if l_ver == "2.4.0" else "VERSION MISMATCH"
        print(f"{'pytorch-lightning':<25} | {status:<15} | v{l_ver}")
    else:
        print(f"{'pytorch-lightning':<25} | FAILED          | Module Not Found")

    # --- SECTION 2: ROOT C++ JIT FUNCTIONALITY ---
    print("\n" + "-" * 90)
    print("ADVANCED ROOT INTERFACE TEST")
    print("-" * 90)
    try:
        import ROOT
        ROOT.gInterpreter.Declare("""
            namespace HEPTools {
                double DeltaR(double eta1, double phi1, double eta2, double phi2) {
                    double deta = eta1 - eta2;
                    double dphi = TVector2::Phi_mpi_pi(phi1 - phi2);
                    return std::sqrt(deta*deta + dphi*dphi);
                }
            }
        """)
        dr_val = ROOT.HEPTools.DeltaR(0.1, 0.2, 0.4, 0.5)
        print(f"{'ROOT (C++ Interpreter)':<25} | SUCCESS         | DeltaR JIT Calculation: {dr_val:.4f}")
    except Exception as e:
        print(f"{'ROOT (C++ Interpreter)':<25} | FAILED          | Error: {str(e)[:40]}")

    # --- SECTION 3: COMPATIBILITY TRAINING PASS ---
    print("\n" + "-" * 90)
    print("FUNCTIONAL TRAINING COMPATIBILITY (SKLearn -> Lightning)")
    print("-" * 90)
    
    if L is None:
        print(f"{'Full Training Pipeline':<25} | SKIPPED         | Lightning module not available")
    else:
        try:
            X = np.random.randn(100, 5)
            y = (X[:, 0] > 0).astype(int)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            train_loader = utils.data.DataLoader(
                utils.data.TensorDataset(torch.tensor(X_scaled, dtype=torch.float32), 
                                         torch.tensor(y, dtype=torch.long)),
                batch_size=8
            )

            class TestModel(L.LightningModule):
                def __init__(self):
                    super().__init__()
                    self.layer = nn.Linear(5, 2)
                    self.loss_fn = nn.CrossEntropyLoss()
                def training_step(self, batch, batch_idx):
                    x, y = batch
                    return self.loss_fn(self.layer(x), y)
                def configure_optimizers(self):
                    return torch.optim.Adam(self.parameters(), lr=1e-3)

            trainer = L.Trainer(max_epochs=1, accelerator="auto", devices=1, 
                                enable_progress_bar=False, logger=False)
            trainer.fit(TestModel(), train_loader)
            print(f"{'Full Training Pipeline':<25} | SUCCESS         | 1 Epoch completed")
        except Exception as e:
            print(f"{'Full Training Pipeline':<25} | FAILED          | Error: {e}")

    print("=" * 90)
    print("VERIFICATION COMPLETE")
    print("=" * 90)

if __name__ == "__main__":
    run_suite()