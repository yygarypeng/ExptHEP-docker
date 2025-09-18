conda create -n py310 python==3.10 -y
conda activate py310

conda install pip numpy pandas scipy matplotlib h5py pytables -y
conda install conda-forge::mplhep -y
conda install conda-forge::root -y
conda install conda-forge::uproot -y

echo "Successfully created and set up the py310 environment with all packages installed."
